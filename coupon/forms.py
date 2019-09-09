from django import forms
from members.models import User
from coupon.models import CouponUser

class RegisterCouponForm(forms.ModelForm):
    input_code = forms.CharField(max_length=20)
    class Meta:
        model = CouponUser
        fields = ['input_code']