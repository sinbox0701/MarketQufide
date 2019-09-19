from django import forms
from .models import Order
from coupon.models import CouponUser
from members.models import User

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email']

'''def GetCouponList(request):
    user = User.objects.get(id=request.user.id)
    coupons = CouponUser.objects.filter(user=user)
    coupon_list = []
    for coupon in coupons:
        coupon_list.append(coupon.name)
    return coupon_list


class CouponSelectForm(forms.ModelForm):
    class Meta:
        model = CouponUser
        fields = ['coupon_select']
        widget = {
            'coupon_select' : forms.Select(attrs=GetCouponList())
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CouponSelectForm, self).__init__(*args,**kwargs)'''
