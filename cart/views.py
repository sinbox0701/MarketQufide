from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .forms import AddProductForm
from .cart import Cart
#from coupon.forms import AddCouponForm

@require_POST
def add(request, product_id): # 제품 정보 전달 받으면 카트 객체에 제품 객체 추가
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], is_update=cd['is_update'])
    return redirect('cart:detail')

def remove(request, product_id): # 카트에서 제품 삭제
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:detail')

def detail(request): # 장바구니 페이지
    cart = Cart(request)
    #add_coupon = AddCouponForm()
    #for product in cart:
        #product['quantity_form'] = AddProductForm(initial={'quantity':product['quantity'], 'is_update':True})
    return render(request, 'cart/detail.html', {'cart': cart})
