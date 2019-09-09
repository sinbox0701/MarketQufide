from django.db import models
from django.contrib.auth.models import AbstractUser
from coupon.models import Coupon
# Create your models here.
class User(AbstractUser):
    mileage = models.IntegerField(default=0)
    #coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)
