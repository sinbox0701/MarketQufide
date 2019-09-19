# Create your views here.
from random import randint

from django.contrib.auth import login as django_login, authenticate, logout as django_logout, get_user_model
from django.shortcuts import render, redirect
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from django.conf import settings

from members.models import Phone
from .forms import SignUpForm, LogInForm

#from django.shortcuts import render, get_object_or_404
from shop.models import Category
from coupon.models import *

from django.http import HttpResponseRedirect
# Create your views here.



User = settings.AUTH_USER_MODEL

def index(request):
    return render(request, 'base.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            User.objects.create_user(email=email, password=raw_password)
            user = authenticate(email=email, password=raw_password)
            django_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    #return render(request, 'member/signup.html', {'form': form})
    return render(request, 'account/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            form.login(request)
            return redirect('index')
    else:
        form = LogInForm()
    return render(request, 'account/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return redirect('index')


def profile(request):
    return render(request, 'members/profile.html')


def verify_page(request):
    return render(request, 'members/verify_phone.html')


def verify_phone(request):
    if request.method == 'POST':
        api_key = settings.COOLSMS_API_KEY
        api_secret = settings.COOLSMS_API_SECRET
        recipient = request.POST.get('phone_number')
        code = ''.join([str(randint(0, 9)) for i in range(6)])

        params = dict()
        params['type'] = 'sms'
        params['to'] = recipient
        params['from'] = settings.SENDER
        params['text'] = 'Verification code: ' + code
        url = 'https://api.coolsms.co.kr/sms/2/send'
        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)

        else:
            print('-----------------------------')
            print('verification code: {code}')
            print('-----------------------------')
            phone = Phone.objects.get(user=request.user)
            phone.verification_code = code
            phone.before_verified = recipient
            phone.save()

        context = {
            'called': True,
        }
    else:
        context = None
    return render(request, 'verify_phone.html', context)


def check_verification_code(request):
    input_code = request.POST.get('verification_code')
    phone = Phone.objects.get(user=request.user)
    if phone.verification_code == input_code:
        phone.number = phone.before_verified
        phone.before_verified = None
        phone.save()
        return render(request, 'members/profile.html')
    context = {
        'called': True,
        'verification_fail': True
    }
    return render(request, 'members/verify_phone.html', context)

def mypage(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'members/mypage.html', context)







