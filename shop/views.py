from django.shortcuts import render, get_object_or_404
from .models import *
from cart.forms import AddProductForm

def product_in_category(request, category_slug=None): # 카테고리 페이지
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(categories=current_category)

    return render(request,'shop/list.html',{'current_category':current_category, 'categories': categories, 'products':products})

def product_detail(request, id, product_slug=None): # 제품 상세 뷰
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request, 'shop/detail.html', {'product':product, 'add_to_cart':add_to_cart, 'categories' : categories})

def home(request) :
    categories = Category.objects.all()
    current_category = None
    banners = Banner.objects.all()
    return render(request, 'shop/home.html', {'categories' : categories, 'current_category' : current_category, 'banners' : banners})

def search(request):
    print("here")
    #products = Product.objects.filter(available_display=True)
    categories = Category.objects.all()
    products = Product.objects.all()
    search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        products = products.filter(name__contains=search_term)
    return render(request, 'shop/search.html',
                  {'products': products, 'search_term' : search_term, 'categories' : categories})
