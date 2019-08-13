from django.shortcuts import render, get_object_or_404
from .models import *
from cart.forms import AddProductForm
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect

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
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    relative_products = Product.objects.filter(company=product.company).exclude(slug=product_slug)
    
    #comment 부분
    #comments = Comment.objects.all()
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        comment_form.instance.author = request.user.id
        comment_form.instance.product_slug = product_slug
        if comment_form.is_valid():
            comment = comment_form.save()
        # models.py에서 document의 related_name을 comments로 해놓았다.

    comment_form = CommentForm()
    comments = Comment.objects.filter(product=product)
    print(comments)
    return render(request, 'shop/detail.html', {'product':product, 'add_to_cart':add_to_cart, 'relative_products': relative_products,
                                                'comments':comments, 'comment_form':comment_form})


def comment(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    comments = Comment.objects.filter(product=product)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = Product.objects.get(id=id)
            comment.author = request.user
            comment.save()
            return redirect('shop:comment', id, product_slug)
    else:
        form = CommentForm()

    return render(request, 'shop/comment.html', {'form': form, 'comments':comments})
 
def update_comment(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    document = get_object_or_404(Document, pk=comment.document.id)

    if request.user != comment.author:
        messages.warning(request, "권한 없음")
        return redirect('shop:comment')

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('shop:comment')
    else:
        form = CommentForm(instance=comment)
    return render(request,'shop/update_comment.html',{'form':form})


def delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author and not request.user.is_staff:
        messages.warning(request, '권한 없음')
        return redirect('shop:comment')

    if request.method == "POST":
        comment.delete()
        return redirect('shop:comment')
    else:
        return render(request, 'shop/delete_comment.html', {'object':comment})

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