from django import forms
from coupon.models import CouponUser, Coupon
from order.models import Order

class RegisterCouponForm(forms.ModelForm):
    input_code = forms.CharField(max_length=20)
    class Meta:
        model = CouponUser
        fields = ['input_code']


'''class SelectCouponForm(forms.Form):
    coupon = forms.ModelChoiceField(queryset=CouponUser.objects.none())

    class Meta:
        model = Order
        fields = ['coupon']

    def __init__(self, user):
        super(SelectCouponForm, self).__init__()
        coupon_ids = CouponUser.objects.filter(user=user).values_list('coupon_id', flat=True)
        for id in coupon_ids:
            self.fields['coupon'].queryset = self.fields['coupon'].queryset | Coupon.objects.filter(id=id)'''