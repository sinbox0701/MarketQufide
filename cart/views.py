from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Option
from .forms import AddProductForm
from .cart import Cart
#from coupon.forms import AddCouponForm

@require_POST
def add(request, product_id): # 제품 정보 전달 받으면 카트 객체에 제품 객체 추가
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    option_ids = request.POST.getlist('option[]')
    options = Option.objects.filter(id__in=option_ids)

    print (request.POST)
    print (options)

    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        for option in options:
            cart.add(product=product, option=option, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')

def remove(request, product_id, option_id): # 카트에서 제품 삭제
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    option = get_object_or_404(Option, id=option_id)
    cart.remove(product, option)
    return redirect('cart:detail')

def detail(request): # 장바구니 페이지
    cart = Cart(request)
    for option in cart:
        option['quantity_form'] = AddProductForm(initial={'quantity':option['quantity'], 'is_update':True})
    #add_coupon = AddCouponForm()
    #for product in cart:
        #product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    return render(request, 'cart/detail.html', {'cart': cart})
