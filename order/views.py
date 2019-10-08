from django.shortcuts import render, get_object_or_404
from .models import *
from cart.cart import Cart
from .forms import OrderCreateForm
# from coupon.forms import SelectCouponForm
from shop.models import *
from django.views.decorators.csrf import csrf_exempt
from coupon.models import *
from members.models import User as mUser
from members.models import Address


@csrf_exempt
def order_create(request):  # 주문서 입력
    cart = Cart(request)
    if request.user.id != None :
        address = Address.objects.get(username=request.user)
        print ("*****************************111")
        if request.method == 'POST':
            print ("*****************************222")
            order_create_form = OrderCreateForm(request.POST)
            if order_create_form.is_valid():
                print ("*****************************333")
                order = order_create_form.save(commit=False)
                order.save()
                for item in cart:
                    print (item['product'])
                    if item['product'] != None:
                        OrderItem.objects.create(order=order, product=item['product'], option=item['option'], price=item['price'], quantity=item['quantity'])
                if 'price_post' in request.POST:
                    print ("*****************************444")
                    price = request.POST['price_post']
                    order_price = Order.objects.get(order=order)
                    order_price.price = price
                    order_price.save()
        else:
            print ("*****************************555")
            order_create_form = OrderCreateForm()
            order = order_create_form.save(commit=False)
            order.zip = address.zip
            order.addr1 = address.addr1
            order.addr2 = address.addr2
            order_create_form = OrderCreateForm(instance=order)
            return render(request, 'order/create.html', {'cart' : cart, 'order_create_form' : order_create_form})

    else:
        if request.method == 'POST':
            order_create_form = OrderCreateForm(request.POST)
            if order_create_form.is_valid():
                order = order_create_form.save(commit=False)
                order.save()
                for item in cart:
                    print (item['product'])
                    if item['product'] != None:
                        OrderItem.objects.create(order=order, product=item['product'], option=item['option'], price=item['price'], quantity=item['quantity'])
                if 'price_post' in request.POST:
                    price = request.POST['price_post']
                    order_price = Order.objects.get(order=order)
                    order_price.price = price
                    order_price.save()
        else:
            order_create_form = OrderCreateForm()
            return render(request, 'order/create.html', {'cart' : cart, 'order_create_form' : order_create_form})

def order_complete(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.get(id=order_id)
    orderitems = OrderItem.objects.filter(order=order)
    sum = 0
    for orderitem in orderitems:
        orderitem.product.count_order+=orderitem.quantity
        orderitem.option.stock-=orderitem.quantity
        orderitem.product.save()
        sum += orderitem.get_item_price()

    if order.price == 0:
        order.price=sum
        order.save()

    order.order_userID = request.user
    order.save()

    return render(request, 'order/created.html', {'order': order})


from django.views.generic.base import View
from django.http import JsonResponse


class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        #if not request.user.is_authenticated:
        #    return JsonResponse({"authenticated":False}, status=403)
        cart = Cart(request)
        #form = OrderCreateForm(mUser,request.POST) #기웅
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], option=item['option'],
                                         price=item['price'], quantity=item['quantity'])
            cart.clear()

            data = {
                "order_id": order.id
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


# 결제 정보 생성
class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        #if not request.user.is_authenticated:
        #    return JsonResponse({"authenticated": False}, status=403)


        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        amount = request.POST.get('amount')

        try:
            merchant_order_id = OrderTransaction.objects.create_new(
                order=order,
                amount=amount
            )
        except:
            merchant_order_id = None

        if merchant_order_id is not None:
            data = {
                "works": True,
                "merchant_id": merchant_order_id
            }
            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


# 결제 검증
class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        #if not request.user.is_authenticated:
        #    return JsonResponse({"authenticated": False}, status=403)


        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        merchant_id = request.POST.get('merchant_id')
        imp_id = request.POST.get('imp_id')
        amount = request.POST.get('amount')

        try:
            trans = OrderTransaction.objects.get(
                order=order,
                merchant_order_id=merchant_id,
                amount=amount
            )
        except:
            trans = None

        if trans is not None:
            trans.transaction_id = imp_id
            trans.success = True
            trans.save()
            order.paid = True
            order.save()

            data = {
                "works": True
            }

            return JsonResponse(data)
        else:
            return JsonResponse({}, status=401)


from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required  # 관리자 권한이 있을때만 호출 가능
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/admin/detail.html', {'order': order})


