from django.shortcuts import render
from members.models import User as mUser
from .forms import RegisterCouponForm
from coupon.models import Coupon, CouponUser
from shop.models import Category
from django.utils import timezone
# Create your views here.

def valid(coupon_code, user):
    coupon_exist_valid = Coupon.objects.filter(code=coupon_code)
    if coupon_exist_valid == None:
        print("coupon doesnt exist")
        return False
    else:
        actual_coupon = coupon_exist_valid.first()
        already_registered_valid = CouponUser.objects.filter(coupon=actual_coupon, user=user)
        if len(already_registered_valid) == 0:
            if timezone.now() > actual_coupon.expiration_date:
                print("check coupon date")
                return False
            else:
                return True

        else:
            print("coupon already registered")
            return False

#쿠폰함/쿠폰등록
def CouponRegister(request):
    categories = Category.objects.all()
    user = mUser.objects.get(id=request.user.id)
    form = RegisterCouponForm(request.POST)

    if form.is_valid():
        input_code = request.POST['input_code']
        v = valid(input_code, user)

        if v==True:
            actual_coupon = Coupon.objects.filter(code=input_code).first()
            new_coupon_user = CouponUser(user=user, coupon=actual_coupon, times_used=0)
            new_coupon_user.save()

    coupons = CouponUser.objects.filter(user=user, times_used=0)
    context = {'categories': categories, 'user': user, 'form': form, 'coupons':coupons}
    return render(request, 'members/coupon.html', context)

