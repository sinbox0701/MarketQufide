from django.urls import path
from .views import *

app_name = 'shop'

urlpatterns = [
    path('', product_in_category, name='product_all'), # 카테고리 선택 없이 상품 전체 노출
    path('<slug:category_slug>/', product_in_category, name='product_in_category'), # 카테고리 선택
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'), # 상품 상세 페이지
]