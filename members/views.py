# Create your views here.
from random import randint
from django.contrib.auth import login as django_login, authenticate, logout as django_logout, get_user_model
from django.shortcuts import render, redirect,get_object_or_404
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from django.conf import settings
from django.http import HttpResponse
from allauth.account.views import SignupView
#from members.models import Phone
from .forms import SignUpForm, LogInForm,SmsForm,ConfirmForm
from .models import SmsSend
from .CertiNum import get_centification_number
#from django.shortcuts import render, get_object_or_404
from shop.models import Category
from coupon.models import *
import datetime

from django.http import HttpResponseRedirect
# Create your views here.


User = settings.AUTH_USER_MODEL

# allauth customizing
class CustomSignupView(SignupView):
    def send_and_confirm(request):
        send_form = SmsForm(data=request.POST)
        # confirm_form = ConfirmForm(request.POST)
        def get_valid_sms_info_and_save():
            get_valid_params = {
                'type': 'sms',
                'to': request.POST.get('msg_getter'),
                'from': settings.SENDER,
                'text': str(get_centification_number(4)),
            }
            send_form.save()
            return get_valid_params
        if request.method == "POST":
            confirm_form = ConfirmForm(request.POST)
            if send_form.is_valid():
                try:
                    params = get_valid_sms_info_and_save()
                    cool = Message(settings.COOLSMS_API_KEY, settings.COOLSMS_API_SECRET)
                    response = cool.send(params)
                    '''
                    success_count = response['success_count']
                    print(success_count)
                    error_count = response['error_count']
                    print(error_count)
                    print('Group ID : {}'.format(response['group_id']))
                    '''
                    if 'error_list' in response:
                        print('Error List : {}'.format(response['error_list']))
                    return redirect('members:test')
                except CoolsmsException as e:
                    return HttpResponse('Error : {} - {}'.format(e.code, e.msg))
            if confirm_form.is_valid():
                try:
                    params2 = dict()
                    #params2['send_time'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    cool = Message(settings.COOLSMS_API_KEY, settings.COOLSMS_API_SECRET)
                    response2 = cool.sent(params2)
                    data = response2['data']
                    #print(data)
                    if request.POST.get('conf') == data[0]['text']:
                            return HttpResponse('okt')
                except CoolsmsException as e:
                    return HttpResponse('Error : {} - {}'.format(e.code, e.msg))
        else:
            send_form = SmsForm()
            confirm_form = ConfirmForm()
        context = {
            'send_form': send_form,
            'confirm_form': confirm_form
        }
        return render(request, 'members/test.html', context)
signup = CustomSignupView.as_view()

# allauth customizing

def index(request):
    return render(request, 'base.html')

'''
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            User.objects.create_user(email=email, password=raw_password)
            user = authenticate(email=email, password=raw_password)
#            django_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()


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

'''
def profile(request):
    return render(request, 'members/profile.html')

'''
def test(request):
    form = SmsForm(data=request.POST)
    def get_valid_sms_info_and_save():
        get_valid_params = {
            'type': request.POST.get('msg_type'),
            'to': request.POST.get('msg_getter'),
            'from': request.POST.get('msg_sender'),
            'text': request.POST.get('msg_text'),
        }
        form.save()
        return get_valid_params

    if request.method == "POST":
        try:
            params = get_valid_sms_info_and_save()
            cool = Message(settings.COOLSMS_API_KEY, settings.COOLSMS_API_SECRET)
            response = cool.send(params)
            success_count = response['success_count']
            print(success_count)
            error_count = response['error_count']
            print(error_count)
            print('Group ID : {}'.format(response['group_id']))

            if 'error_list' in response:
                print('Error List : {}'.format(response['error_list']))
            context = {
                'form': form,
                'success_count': success_count,
                'error_count': error_count,
            }
            return render(request, 'members/test.html', context)

        except CoolsmsException as e:
            return HttpResponse('Error : {} - {}'.format(e.code, e.msg))
    else:
        form = SmsForm()
    context = {
        'form': form,
    }
    return render(request, 'members/test.html', context)
'''

def mypage(request):
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'members/mypage.html', context)







