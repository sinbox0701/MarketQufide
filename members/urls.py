from django.contrib import admin
from django.urls import path
from members.views import signup, profile
from django.urls import re_path
from .views import *
from coupon.views import coupon



app_name = 'members'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    #path('signup/', sms_send, name='sms_send'),
    #path('login/', login, name='login'),
    #path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('mypage/', mypage, name='mypage'),
    path('mypage/coupon', coupon, name="coupon"),
    path('test/', CustomSignupView.send_and_confirm, name='test'),


    #path('admin/', admin.site.urls), # 이유진
]

