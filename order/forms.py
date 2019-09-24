from django import forms
from .models import Order
from coupon.models import CouponUser, Coupon
import itertools


class OrderCreateForm(forms.ModelForm):
    coupon = forms.ModelChoiceField(queryset=CouponUser.objects.none())

    def __init__(self, user):
        super(OrderCreateForm, self).__init__()
        coupon_ids = CouponUser.objects.filter(user=user).values_list('coupon_id', flat=True)
        for id in coupon_ids:
            self.fields['coupon'].queryset = self.fields['coupon'].queryset | Coupon.objects.filter(id=id)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email','zip','addr1','addr2','coupon']



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

