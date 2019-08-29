from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'categories', 'price', 'available_display', 'available_order', 'created', 'updated']
    list_filter = ['available_display', 'created', 'updated', 'categories']
    prepopulated_fields = {'slug': ('name',)} # slug 필드는 name 필드의 값에 따라 자동 설정 가능
    list_editable = ['price', 'available_display', 'available_order'] # 주요값 바로 변경 가능


admin.site.register(Banner)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Company)
admin.site.register(Delivery)
admin.site.register(Comment)
admin.site.register(Collection)
admin.site.register(Event)