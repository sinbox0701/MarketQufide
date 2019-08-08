from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


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


class Theme(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    meta_description = models.TextField(blank=True)  # Search Engine Optimization

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])


class Option(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    add_price = models.IntegerField()

    def __str__(self):
        return '{} // {}'.format(self.name, self.add_price)


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

    theme = models.ManyToManyField(Theme)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # 가격
    stock = models.PositiveIntegerField() # 재고
    company = models.ForeignKey(Company, null=True, on_delete=models.SET_NULL)
    available_display = models.BooleanField('Display', default=True) # 상품 노출 여부
    available_order = models.BooleanField('Order', default=True) # 상품 주문 가능 여부

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

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
