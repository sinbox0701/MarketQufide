from django.shortcuts import render
from shop.models import *
from .forms import InquiryForm

# Create your views here.
def index(request):
    categories = Category.objects.all()
    inquiry = Inquiry.objects.all()
    context = {
        'categories' : categories,
        'inquiry' : inquiry,
    }
    return render(request, 'qna/index.html', context)

def inquiry_add(request):
    form = InquiryForm()
    context = {
        'form' : form,
    }
    return render(request, 'qna/index.html', context)
