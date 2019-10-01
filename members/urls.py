from django.contrib import admin
from django.urls import path
from members.views import signup, login, logout, profile, verify_phone, check_verification_code, verify_page
from django.urls import re_path
from .views import *
from coupon.views import coupon



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
    path('mypage/coupon', coupon, name="coupon"),
    path('mypage/address', address, name="address"),
    path('mypage/address/add', add_address, name="add_address"),
    path('mypage/address/<int:id>/update', update_address, name="update_address"),
    path('mypage/address/<int:id>/delete', delete_address, name="delete_address"),
    path('profile/delete', delete, name='delete'),
    path('mypage/order', order, name='order'),
    path('findID/', findID, name='findID'),
    #path('admin/', admin.site.urls), # 이유진
]

