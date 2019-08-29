from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

#from django.contrib.auth.models import User
from django.conf import settings
# ----- 인증번호 -----
import requests
from random import randint
from model_utils.models import TimeStampedModel
# -------------

from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from tagging.fields import TagField


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.SET_NULL)
    slug = models.SlugField()
    meta_description = models.TextField(blank=True)  # Search Engine Optimization

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('parent', 'slug',)
        verbose_name = 'category'  # 관리자 페이지에서 객체가 단수일때 값
        verbose_name_plural = 'categories'  # 곤리자 페이지에서 객체가 복수일때 값

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]
        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i + 1]))
        return slugs

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category', args=[self.slug])

class Delivery(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField()
    meta_description = models.TextField(blank=True)
    price = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.name)


class Company(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField()
    delivery = models.ManyToManyField(Delivery)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    categories = TreeForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    # 카테고리 모델과 관계 만들기, 카테고리를 지워도 상품은 남아있어야함
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    image2 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    image3 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    image4 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    image5 = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)
    description = models.TextField(blank=True)
    #meta_description = models.TextField(blank=True)
    tag_description = TagField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=0) # 가격
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    available_display = models.BooleanField('Display', default=True) # 상품 노출 여부
    available_order = models.BooleanField('Order', default=True) # 상품 주문 가능 여부
    count_order = models.IntegerField(default=0) # 팔린 갯수


    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    count_order = models.IntegerField(default=0)
    sale_percent = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']] # 멀티 컬럼 색인 기능

    def __str__(self):
        return self.name

    def get_cat_list(self):  # for now ignore this instance method,
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def get_recipe_absolute_url(self):
        return reverse('shop:recipe_detail', args=[self.id, self.slug])


class Option(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    product = models.ForeignKey(Product, on_delete=True, null=True)
    content = models.TextField()
    add_price = models.IntegerField()
    stock = models.IntegerField(default=0)

    def __str__(self):
        return '{} // {} // {}'.format(self.product, self.name, self.add_price)


class Comment(models.Model):

    product = models.ForeignKey(Product, on_delete=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='comments')
    comment_created = models.DateTimeField(auto_now_add=True)
    comment_updated = models.DateTimeField(auto_now=True)
#    comment_thumbnail_url = models.TextField(max_length=20)
    like = models.IntegerField(choices=list(zip(range(0, 6), range(0, 6))))
    comment_text = models.TextField()
    best = models.BooleanField(default=False)

    def __str__(self):
        return (self.author.username if self.author else "무명") + "의 댓글"


class Banner(models.Model):
    name = models.CharField(blank=True, max_length=30)
    image = models.ImageField()
    url = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AuthSMS(TimeStampedModel):
    phone_number = models.CharField(verbose_name='휴대폰 번호', primary_key=True, max_length=11)
    auth_number = models.IntegerField(verbose_name='인증 번호')

    class Meta:
        db_table = 'auth_sms'

    def save(self, *args, **kwargs):
        self.auth_number = randint(1000,10000)
        super.save(*args, **kwargs)
        self.send_sms() # 인증번호가 담긴 SMS를 전송

    def send_sms(self):
        url = 'https://api-sens.ncloud.com/v1/sms/services/ncp:sms:kr:256764018047:marketqufide/messages/'
        data = {
            "type": "SMS",
            "from": "01056373374", # 이후 변경
            "to": [self.phone_number],
            "content": "[테스트] 인증 번호 [{}]를 입력해주세요.".format(self.auth_number)
        }
        headers = {
                      "Content-Type": "application/json",
                      "x-ncp-auth-key": 'HW9MQH1PDRFbSXiORKXE',
                  "x-ncp-service-secret": '82ac2516914143deb1ad0d0a808f822e',
        }
        requests.post(url, json=data, headers=headers)


class Collection(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    title_image = models.ImageField()
    description = models.TextField(blank=True)
    products = models.ManyToManyField(Product)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:collection_detail', args=[self.slug])


class Event(models.Model):
    title_image = models.ImageField()
    name = models.CharField(max_length=30)
    content = models.ImageField()
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True, default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:event_detail', args=[self.slug])

