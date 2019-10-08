# Create your views here.
from random import randint
from django.contrib.auth import login as django_login, authenticate, logout as django_logout, get_user_model
from django.shortcuts import render, redirect,get_object_or_404
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException
from django.conf import settings
from django.http import HttpResponse
from allauth.account.views import *
#from members.models import Phone

from .forms import *

from .models import SmsSend
from .CertiNum import get_centification_number
from members.models import *
from kwShop.forms import CustomSignupForm
#from django.shortcuts import render, get_object_or_404
from shop.models import Category
from coupon.models import *
import datetime
from order.models import *
from kwShop.forms import *
from django.http import HttpResponseRedirect
# Create your views here.

#User = settings.AUTH_USER_MODEL

# allauth customizing
class CustomSignupView(SignupView):
    #template_name = "members/signup." + app_settings.TEMPLATE_EXTENSION
    #form_class = CustomSignupForm

    success_url =  '/test/'

    def get_success_url(self):
        return '/test/'

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
                            return HttpResponseRedirect('/')
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
                # params2['send_time'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                cool = Message(settings.COOLSMS_API_KEY, settings.COOLSMS_API_SECRET)
                response2 = cool.sent(params2)
                data = response2['data']
                # print(data)
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
    return render(request, 'members/signup.html', context)
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


def relogin(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.clean_verify_password()
            form.login(request)
            return redirect('index')
    else:
        form = LogInForm()
    return render(request, 'account/relogin.html', {'form': form})
'''

def index(request):
    return render(request, 'base.html')

def address(request):
    member = get_object_or_404(User, username=request.user)
    addresses = Address.objects.filter(username=request.user)


    return render(request, 'members/address.html', {'addresses':addresses})


def update_address(request, id):
    address = get_object_or_404(Address, id=id)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('members:address')
    else:
        form = AddressForm(instance=address)

    return render(request, 'members/update_address.html', {'form': form})

def delete_address(request, id):
    address = get_object_or_404(Address, id=id)

    if request.method == "POST":
        address.delete()
        return redirect('members:address')
    else:
        return render(request, 'members/delete_address.html', {'object':address})


def add_address(request):
    member = get_object_or_404(User, username=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.username=request.user
            address.save()
            print (address)
            return redirect('members:address')
    else:
        form = AddressForm(instance=member)

    return render(request, 'members/add_address.html', {'form': form})


def order(request):
    try:
        member = get_object_or_404(User, username=request.user)
        orders = Order.objects.filter(order_userID=member, paid=True)
        for order in orders:
            orderitems = OrderItem.objects.filter(order=order)
        count=0
        for orderitem in orderitems:
            count+=1
        return render(request, 'members/order.html', {'orders':orders, 'orderitem':orderitems[0], 'count':count-1})
    except:
        return render(request, 'members/order.html', {'orders':None, 'orderitems':None})

def order_detail(request, orderno):
    order= get_object_or_404(Order, orderno=orderno)
    orderitems = OrderItem.objects.filter(order=order)
    print(orderitems)
    return render(request, 'members/order_detail.html',
                  {'order': order, 'orderitems': orderitems})


def findID(request):
    if request.method == "POST":
        form = findIDForm(request.POST or None)
        if form.is_valid():
            try :
                member = User.objects.get(name=form['name'].value(), phone=form['phone'].value())
                return render(request, 'members/confirmID.html', {'member':member})
            except:
                return render(request, 'members/wrongID.html')

    else:
        form = findIDForm(request.POST)
        return render(request, 'members/findID.html', {'form':form})


'''
def logout(request):
    django_logout(request)
    return redirect('index')

'''
def profile(request):
    print(request.user)
    member = get_object_or_404(User, username=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('members:profile')
    else:
        form = ProfileForm(instance=member)

    return render(request, 'members/profile.html', {'form':form})

def delete(request):
    member = get_object_or_404(User, username=request.user)
    if request.method == "POST":
        member.delete()
        return redirect('shop:product_all')
    return render(request, 'members/memberdelete.html')

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







