from django.urls import path
from django.urls import re_path
from .views import *
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
    #path('', category, name='product_all'), # 카테고리 선택 없이 상품 전체 노출

    path('', home, name='product_all'),

    #path('', search),

    path('search/', search, name='search'),
    path('<slug:category_slug>/', category, name='category'),  # 카테고리 선택
    #path('', product_in_category, name='product_all'), # 카테고리 선택 없이 상품 전체 노출
    #path('<slug:category_slug>/', product_in_category, name='product_in_category'), # 카테고리 선택
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'), # 상품 상세 페이지
    path('<int:id>/<product_slug>/comment/', comment, name='comment'),
    path('<int:id>/<product_slug>/comment/delete', delete_comment, name="delete_comment"),
    path('<int:id>/<product_slug>/comment/update', update_comment, name="update_comment"),
]
