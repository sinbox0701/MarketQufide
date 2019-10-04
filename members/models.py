from django.db import models
from django.contrib.auth.models import AbstractUser # 유진이
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.conf import settings
from .CertiNum import get_centification_number

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
        #Phone.objects.create(user=user)
        return user

    def create_user(self, email, password=None):
        return self._create_user(email, password)


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


class Address(models.Model):
    addr_name = models.CharField(max_length=30)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    zip = models.CharField(max_length=20)
    addr1 = models.CharField(max_length=250)
    addr2 = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)


class SmsSend(models.Model):
    MSG_TYPE_CHOICES = (
        ('sms', 'sms'),
    )
    msg_type = models.CharField(max_length=3, choices=MSG_TYPE_CHOICES, default='sms')
    # IntegerField로 하면 휴대폰 전화번호 첫자리 '0' 이 사라진다.
    msg_getter = models.CharField(max_length=20, blank=False)
    msg_sender = models.CharField(max_length=20, blank=False, default=settings.SENDER)
    msg_text = models.CharField(max_length=4)

    def __str__(self):
        return self.msg_text

