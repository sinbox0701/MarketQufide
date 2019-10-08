from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product, Option, Company
from .forms import AddProductForm
from .cart import Cart
#from coupon.forms import AddCouponForm

@require_POST
def add(request, product_id): # 제품 정보 전달 받으면 카트 객체에 제품 객체 추가
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    print(request.POST)
    option_id = request.POST['option_id']
    option = get_object_or_404(Option, id=option_id)


    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
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
    companies = Company.objects.none()
    sale_products = Product.objects.all().exclude(sale_percent=0).order_by('-sale_percent')[:8]
    user = request.user
    for item in cart:
        item['quantity_form'] = AddProductForm(initial={'option_id':item['option'].id, 'quantity':item['quantity'], 'is_update':True})
        companies  = companies | Company.objects.filter(name=item['product'].company)
    #add_coupon = AddCouponForm()
    #for product in cart:
        #product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    delivery_company_count = 0
    for company in companies:
        price_sum = 0
        for item in cart:
            if item['product'].company == company:
                price_sum += item['price'] * item['quantity']
        if price_sum < 30000:
            delivery_company_count += 1
    delivery_fee = 3000 * delivery_company_count
    total_price_without_discount = 0
    for item in cart:
        total_price_without_discount += item['product'].price * item['quantity']

    return render(request, 'cart/detail.html',
                  {'cart': cart, 'companies': companies, 'user': user, 'delivery_fee': delivery_fee,
                   'total_price_without_discount': total_price_without_discount, 'sale_products': sale_products})
