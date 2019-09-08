#from django.shortcuts import render, get_object_or_404
from shop.models import Category
from django.shortcuts import render, redirect
from coupon.models import *

from django.http import HttpResponseRedirect
# Create your views here.

def mypage(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'members/mypage.html', context)







