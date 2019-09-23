from django.contrib import admin
from django.urls import path
from members.views import signup, login, logout, profile, verify_phone, check_verification_code, verify_page
from django.urls import re_path
from .views import *
from coupon.views import CouponRegister



app_name = 'members'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('verify_page/', verify_page, name='verify_page'),
    path('verify_phone/', verify_phone, name='verify_phone'),
    path('check_verification_code/', check_verification_code, name='check_verification_code'),
    path('mypage/', mypage, name='mypage'),
    path('mypage/coupon', CouponRegister, name="CouponRegister"),
    #path('admin/', admin.site.urls), # 이유진
]

