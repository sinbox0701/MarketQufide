from django.db import models
from django.contrib.auth.models import AbstractUser # 유진이
from coupon.models import Coupon
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# Create your models here.

#class User(AbstractUser):
#    mileage = models.IntegerField(default=0)
#    coupon = models.ManyToManyField(Coupon)


class UserManager(BaseUserManager):
    def _create_user(self, email, password):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save()
        Phone.objects.create(user=user)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password)

class Phone(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, null=True)
    before_verified = models.CharField(max_length=16, null=True)
    verification_code = models.CharField(max_length=6, null=True)

class Marketing(models.Model):
    name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser): # 원래는 AbstractBaseUser
    mileage = models.IntegerField(default=0)

    #coupon = models.ManyToManyField(Coupon)
    #email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    #USERNAME_FIELD = 'email'
    marketing = models.ManyToManyField(Marketing, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, null=True, blank=True)

    objects = UserManager()
