from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
    path('', category, name='product_all'), # 카테고리 선택 없이 상품 전체 노출
    path('<slug:category_slug>/', category, name='category'), # 카테고리 선택
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'), # 상품 상세 페이지
]
