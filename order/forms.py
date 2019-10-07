from django import forms
from .models import Order
from coupon.models import CouponUser, Coupon
import itertools


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['name', 'email','zip','addr1','addr2','phone','orderco']

    def __init__(self, *args, **kwargs):
        super(OrderCreateForm, self).__init__(*args,**kwargs)




'''
class CouponSelectForm(forms.ModelForm):
    coupon_select = forms.ChoiceField(choices=[])

    class Meta:
        model = CouponUser
        fields=['coupon_select']

    def __init__(self, user, *args, **kwargs):
        super(CouponSelectForm, self).__init__(*args, **kwargs)
        #cps = set(coupon.coupon.name for coupon in CouponUser.objects.filter(user=user))
        #coupon_list = filter(lambda x: x.name not in cps, coupon_list)
        self.fields['coupon_select'] = forms.ChoiceField(choices=get_answer_by_something())

    def querySet_to_list(qs):
        """
        this will return python list<dict>
        """
        return [dict(q) for q in qs]

    def get_answer_by_something(request):
        ss = CouponUser.objects.filter(user=user).values()
        querySet_to_list(ss)  # python list return.(json-able)
'''

