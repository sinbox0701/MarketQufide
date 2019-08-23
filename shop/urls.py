from django.urls import path
from django.urls import re_path
from .views import *
from django.views.generic import TemplateView

app_name = 'shop'

urlpatterns = [
    path('', home, name='product_all'),
    path('search/', search, name='search'),
    path('best_item/', best_item, name="best_item"),
    path('new_item/', new_item, name="new_item"),
    path('frugal_shopping/', frugal_shopping, name="frugal_shopping"),
    path('event/', event, name="event"),
    path('event/<slug:event_slug>', event_detail, name="event_detail"),
    path('recipe/', recipe, name="recipe"),
    path('recipe/<int:id>/<slug:product_slug>', recipe_detail, name="recipe_detail"),
    path('collection/', collection, name='collection'),
    path('collection/<slug:collection_slug>', collection_detail, name="collection_detail"),
    path('search/', search, name='search'),
    path('commentselect/', comment_select, name='comment_select'),  
    path('<slug:category_slug>/', category, name='category'),  # 카테고리 선택
    #path('', product_in_category, name='product_all'), # 카테고리 선택 없이 상품 전체 노출
    #path('<slug:category_slug>/', list, name='product_in_category'), # 카테고리 선택 --> 윤기 형
    #path('<slug:category_slug>/', product_in_category, name='product_in_category'), # 카테고리 선택 --> 우리
    path('<int:id>/<slug:product_slug>/', product_detail, name='product_detail'), # 상품 상세 페이지
    path('<int:id>/<product_slug>/comment/', comment, name='comment'),
    path('comment/<int:id>/', comment_detail, name='comment_detail'),
    path('<int:id>/<product_slug>/comment/delete', delete_comment, name="delete_comment"),
    path('<int:id>/<product_slug>/comment/update', update_comment, name="update_comment"),
]
