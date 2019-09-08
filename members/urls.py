from django.urls import path
from .views import *
from coupon.views import coupon


app_name = 'members'

urlpatterns = [
    path('mypage/', mypage, name='mypage'),
    path('mypage/coupon', coupon, name="coupon")
    #path('admin/', admin.site.urls),
]
