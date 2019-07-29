from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True) # 카테고리 이름, db_index=True로 하면 인덱스 열을  이름으로 설정 가능
    meta_description = models.TextField(blank=True) # Search Engine Optimization
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    # 카테고리와 상품 모두 설정, 상품명등 을 이용하여 URL을 만듦, allow_unicode=True로 영문 이외에 값도 설정

    class Meta:
        ordering = ['name']
        verbose_name = 'category' # 관리자 페이지에서 객체가 단수일때 값
        verbose_name_plural = 'categories' # 곤리자 페이지에서 객체가 복수일때 값

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])

class Product(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    # 카테고리 모델과 관계 만들기, 카테고리를 지워도 상품은 남아있어야함
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # 가격
    stock = models.PositiveIntegerField() # 재고

    available_display = models.BooleanField('Display', default=True) # 상품 노출 여부
    available_order = models.BooleanField('Order', default=True) # 상품 주문 가능 여부

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']] # 멀티 컬럼 색인 기능

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
