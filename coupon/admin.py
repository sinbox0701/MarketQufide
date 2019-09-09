from django.contrib import admin
from .models import *
# Register your models here.
class CouponUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'coupon', 'times_used']

admin.site.register(CouponUser, CouponUserAdmin)
admin.site.register(Coupon)
admin.site.register(Discount)