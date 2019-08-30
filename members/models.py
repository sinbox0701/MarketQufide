from django.db import models
from django.contrib.auth.models import AbstractUser
from django_simple_coupons.models import Coupon
# Create your models here.
class User(AbstractUser):
    mileage = models.IntegerField(default=0)
    coupon = models.ManyToManyField(Coupon)
