from django.shortcuts import render, get_object_or_404
from .models import *
from cart.forms import AddProductForm
from .forms import *

def product_in_category(request, category_slug=None): # 카테고리 페이지
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(categories=current_category)

    return render(request,'shop/list.html',{'current_category':current_category, 'categories': categories, 'products':products})

def product_detail(request, id, product_slug=None): # 제품 상세 뷰
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    #comment 부분
    #comments = Comment.objects.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        comment_form.instance.author_id = request.user.id
        comment_form.instance.product_slug = product_slug
        if comment_form.is_valid():
            comment = comment_form.save()

        # models.py에서 document의 related_name을 comments로 해놓았다.

    comment_form = CommentForm()
    comments = Comment.objects.filter(product=product)
    print(comments)
    return render(request, 'shop/detail.html', {'product':product, 'add_to_cart':add_to_cart, 'comments':comments,'comment_form':comment_form})


