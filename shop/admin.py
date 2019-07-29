from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin): # 카테고리 옵션 클래스
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # slug 필드는 name 필드의 값에 따라 자동 설정 가능

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'categories', 'price', 'stock', 'available_display', 'available_order', 'created', 'updated']
    list_filter = ['available_display', 'created', 'updated', 'categories']
    prepopulated_fields = {'slug': ('name',)} # slug 필드는 name 필드의 값에 따라 자동 설정 가능
    list_editable = ['price', 'stock', 'available_display', 'available_order'] # 주요값 바로 변경 가능

admin.site.register(Product, ProductAdmin)

