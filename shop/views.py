from django.shortcuts import render, get_object_or_404
from .models import *
from cart.forms import AddProductForm


def category(request, category_slug=None): # 카테고리 페이지
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)
    results = Product.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        if current_category.is_child_node():
            results = products.filter(categories=current_category)
        else:
            results = products.filter(categories=current_category)
            for slug in current_category.get_descendants(include_self=True):
                results = results | products.filter(categories=slug)

    return render(request,'shop/list.html', {'current_category': current_category, 'categories': categories, 'products': results})



def product_detail(request, id, product_slug=None): # 제품 상세 뷰
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    relative_products = Product.objects.filter(company=product.company).exclude(slug=product_slug)
    return render(request, 'shop/detail.html', {'product':product, 'add_to_cart':add_to_cart, 'relative_products': relative_products})


