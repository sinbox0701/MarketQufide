from django.contrib import admin
from django.urls import path
from members.views import *
from django.urls import re_path
from .views import *
from coupon.views import coupon



app_name = 'members'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('signup/', send_and_confirm, name='send_and_confirm'),

    #path('signup/', sms_send, name='sms_send'),
    #path('login/', login, name='login'),
    #path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('mypage/', mypage, name='mypage'),
    path('mypage/coupon', coupon, name="coupon"),
    path('test/', send_and_confirm, name='test'),
    path('mypage/address', address, name="address"),
    path('mypage/address/add', add_address, name="add_address"),
    path('mypage/address/<int:id>/update', update_address, name="update_address"),
    path('mypage/address/<int:id>/delete', delete_address, name="delete_address"),
    path('profile/delete', delete, name='delete'),
    path('mypage/order', order, name='order'),
    path('mypage/order/<orderno>/', order_detail, name="order_detail"),
    path('findID/', findID, name='findID'),
    #path('admin/', admin.site.urls), # 이유진
]

