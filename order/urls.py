from django.urls import path
from .views import *
from django.contrib import admin
from members.views import *
from django.urls import re_path


app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('create_ajax/', OrderCreateAjaxView.as_view(), name='order_create_ajax'),
    path('checkout/', OrderCheckoutAjaxView.as_view(), name='order_checkout'),
    path('validation/', OrderImpAjaxView.as_view(), name='order_validation'),
    path('complete/', order_complete, name='order_complete'),
    path('admin/<int:order_id>/', admin_order_detail, name='admin_order_detail')

]