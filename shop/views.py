from django.shortcuts import render, get_object_or_404
from .models import *
from cart.forms import AddProductForm
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

# ------- 인증번호 -------
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models as m
# ------------------

from django.db.models import Count
from django.db.models import Max, Min
from django.db.models import Q
from datetime import datetime, timedelta




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

    order = ''
    if request.method == "GET":
        if 'orderby' in request.GET:
            order = request.GET['orderby']
            print (order)

        if order == 'review':
            results = results.annotate(comment_count=Count("comment")).order_by("-comment_count")
            context = {'current_category': current_category, 'categories': categories, 'products': results}
            return render(request,'shop/list.html', context)
        elif order == 'like':
            results = results.annotate(comment_like=Max("comment__like")).order_by('-comment_like')
            context = {'current_category': current_category, 'categories': categories, 'products': results}
            return render(request,'shop/list.html', context)
        elif order == 'lowprice':
            results = results.order_by('price')
            context = {'current_category': current_category, 'categories': categories, 'products': results}
            return render(request,'shop/list.html', context)
        elif order == 'highprice':
            results = results.order_by('-price')
            context = {'current_category': current_category, 'categories': categories, 'products': results}
            return render(request,'shop/list.html', context)
        elif order == 'date':
            results = results.order_by('created')
            context = {'current_category': current_category, 'categories': categories, 'products': results}
            return render(request,'shop/list.html', context)
        else:
            results = results.order_by('-count_order')
            context = {'current_category': current_category, 'categories': categories, 'products': results}
            return render(request, 'shop/list.html', context)

    context = {'current_category': current_category, 'categories': categories, 'products': results}
    return render(request,'shop/list.html', context)



def product_detail(request, id, product_slug=None): # 제품 상세 뷰
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductForm(initial={'quantity':1})
    relative_products = Product.objects.filter(company=product.company).exclude(slug=product_slug)
    recipes = Recipe.objects.filter(products=product)


    #comment 부분
    comments = Comment.objects.filter(product=product)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        comment_form.instance.author = request.user.id
        comment_form.instance.product_slug = product_slug
        if comment_form.is_valid():
            comment = comment_form.save()
        # models.py에서 document의 related_name을 comments로 해놓았다.

    comment_form = CommentForm()

    order=''
    if request.method == "GET":
        if 'orderby' in request.GET:
            order = request.GET['orderby']

        if order == 'like':
            comments = comments.order_by('-like')
            return render(request, 'shop/detail.html',
                          {'product': product, 'add_to_cart': add_to_cart, 'relative_products': relative_products,
                           'comments': comments, 'comment_form': comment_form, 'options': options})
        elif order == 'date':
            comments = comments.order_by('-comment_created')
            return render(request, 'shop/detail.html',
                          {'product': product, 'add_to_cart': add_to_cart, 'relative_products': relative_products,
                           'comments': comments, 'comment_form': comment_form, 'options': options})

    options = Option.objects.filter(product=product)


    return render(request, 'shop/detail.html', {'categories':categories, 'product':product, 'add_to_cart':add_to_cart, 'relative_products': relative_products,
                                                'comments':comments, 'comment_form':comment_form, 'options':options, 'recipes':recipes})



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

    order = ''
    if request.method == "GET":
        if 'orderby' in request.GET:
            order = request.GET['orderby']

        if order == 'like':
            comments = comments.order_by('-like')
            return render(request, 'shop/comment.html', {'form': form, 'comments':comments, 'product':product})

        elif order == 'date':
            comments = comments.order_by('-comment_created')
            return render(request, 'shop/comment.html', {'form': form, 'comments':comments, 'product':product})

    return render(request, 'shop/comment.html', {'form': form, 'comments':comments, 'product':product})



def comment_detail(request, id):
    comment = Comment.objects.get(id=id)
    form = CommentForm()

    return render(request, 'shop/comment_detail.html', {'comment':comment, 'form':form})



def delete_comment(request, id):

    comment = Comment.objects.get(id=id)
    product = get_object_or_404(Product, slug=comment.product.slug)

    if request.user != comment.author and not request.user.is_staff:
        messages.warning(request, '권한 없음')
        return redirect('shop:comment', product.id, product.slug)

    if request.method == "POST":
        comment.delete()
        return redirect('shop:comment', product.id, product.slug)
    else:
        return render(request, 'shop/delete_comment.html', {'object':comment})



def update_comment(request, id):

    comment = Comment.objects.get(id=id)
    product = get_object_or_404(Product, slug=comment.product.slug)


    if request.user != comment.author:
        messages.warning(request, "권한 없음")
        return redirect('shop:comment', product.id, product.slug)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('shop:comment', product.id, product.slug)
    else:
        form = CommentForm(instance=comment)

    return render(request,'shop/update_comment.html', {'form':form})



def comment_select(request):
    comments = Comment.objects.all()

    if request.method == 'POST':
        select = request.POST.getlist('select')
        best_comments = Comment.objects.filter(id__in=select)
        false_comments = Comment.objects.all().exclude(id__in=select)
        for best_comment in best_comments:
            best_comment.best=True
            best_comment.save()
        for false_comment in false_comments:
            false_comment.best=False
            false_comment.save()

    return render(request, 'shop/commentselect.html', {'comments': comments})



def home(request) :
    categories = Category.objects.all()
    current_category = None
    banners = Banner.objects.all()
    comments = Comment.objects.filter(best=True)


    return render(request, 'shop/home.html', {'categories' : categories, 'current_category' : current_category, 'banners' : banners, 'comments': comments})



def search(request, search_term = ''):
    products = Product.objects.all()
    categories = Category.objects.all()
    if 'search' in request.GET:
        search_term = request.GET['search']
        products = products.filter(Q(name__contains=search_term)|Q(tag_description__contains=search_term))
        print (search_term)
    return render(request, 'shop/search.html',
                  {'products': products, 'search_term' : search_term, 'categories' : categories})


def best_item(request):
    categories = Category.objects.all()
    products = Product.objects.order_by('-count_order')[:10]
    context={'categories' : categories, 'products' : products}
    return render(request, 'shop/best_item.html', context)


def new_item(request):
    categories = Category.objects.all()
    now = datetime.today()
    start_dt = now - timedelta(days=30)

    products = Product.objects.filter(created__gte=start_dt)

    context = {'categories': categories, 'products' : products}
    return render(request, 'shop/new_item.html', context)

def frugal_shopping(request):
    categories = Category.objects.all()
    products = Product.objects.all().exclude(sale_percent=0)
    context = {'categories': categories, 'products': products}
    return render(request, 'shop/frugal_shopping.html', context)

def collection(request):
    categories = Category.objects.all()
    collections = Collection.objects.all()
    context = {'categories':categories, 'collections':collections}
    return render(request, 'shop/collection.html', context)

def collection_detail(request, collection_slug):
    categories = Category.objects.all()
    collection = get_object_or_404(Collection, slug=collection_slug)
    selected_products = collection.products.all()
    context = {'categories':categories, 'selected_products':selected_products, 'collection':collection}
    return render(request, 'shop/collection_detail.html', context)

def event(request):
    categories = Category.objects.all()
    events = Event.objects.all()
    context = {'categories': categories, 'events' : events}
    return render(request, 'shop/event.html', context)

def event_detail(request, event_slug=None):
    categories = Category.objects.all()
    event = get_object_or_404(Event, slug=event_slug)
    context = {'categories' : categories, 'event' : event}
    return render(request, 'shop/event_detail.html', context)



class AuthSMS(APIView):
    def post(self, request):
        try:
            p_num = request.data['phone_number']
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            m.Auth.objects.update_or_create(phone_number=p_num)
            return Response({'message': 'OK'})

def recipe(request):
    categories = Category.objects.all()
    recipes = Recipe.objects.all()
    context = {'categories':categories, 'recipes':recipes}
    return render(request, 'shop/recipe.html', context)

def recipe_detail(request, id, recipe_slug=None):
    categories = Category.objects.all()
    recipe = get_object_or_404(Recipe, id=id, slug=recipe_slug)
    query = Recipe.objects.filter(id=id, slug=recipe_slug).select_related().values('products')
    products = []
    for q in query:
        products.append(Product.objects.get(id=q['products']))

    context = {'categories': categories, 'recipe': recipe, 'products':products}
    return render(request, 'shop/recipe_detail.html', context)


