from django.contrib import admin
from .models import User,SmsSend
# Register your models here.
admin.site.register(User)
admin.site.register(SmsSend)
admin.site.register(Marketing)
admin.site.register(Address)

