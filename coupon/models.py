from django.db import models
from django.conf import settings
from django.utils import timezone
from .coupons import get_random_code
from members.models import User as mUser
# Create your models here.

class CouponUser(models.Model):
    user = models.ForeignKey(mUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE)
    times_used = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)



class Coupon(models.Model):
    code = models.CharField(max_length=16, default=get_random_code)
    #discount = models.ForeignKey('Discount', on_delete=models.CASCADE)
    created = models.DateTimeField()
    name = models.CharField(max_length=20)
    expiration_date = models.DateTimeField()
    minimum_price = models.IntegerField()
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def use_coupon(self, user):
        coupon_user = CouponUser.objects.get(user=user, coupon=self)
        coupon_user.times_used += 1
        coupon_user.save()

    '''
    def get_discount(self):
        return {
            "value": self.discount.value,
            "is_percentage": self.discount.is_percentage
        }

    def get_discounted_value(self, initial_value):
        discount = self.get_discount()
        if discount['is_percentage']:
            new_price = initial_value - ((initial_value * discount['value']) / 100)
            new_price = new_price if new_price >= 0.0 else 0.0
        else:
            new_price = initial_value - discount['value']
            new_price = new_price if new_price >= 0.0 else 0.0
        return new_price
    '''
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Coupon, self).save(*args, **kwargs)



