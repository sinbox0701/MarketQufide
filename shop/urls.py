from django.urls import path
from django.urls import re_path
from .views import *
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
    path('', home, name='product_all'),
    path('search/', search, name='search'),
    path('commentselect/', comment_select, name='comment_select'),
    path('<slug:category_slug>/', category, name='category'),  # 카테고리 선택
    path('<slug:category_slug>/', list, name='product_in_category'), # 카테고리 선택
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'), # 상품 상세 페이지
    path('<int:id>/<product_slug>/comment/', comment, name='comment'),
    path('comment/<int:id>/', comment_detail, name='comment_detail'),
    path('comment/<int:id>/delete/', delete_comment, name="delete_comment"),
    path('comment/<int:id>/update/', update_comment, name="update_comment"),
]
