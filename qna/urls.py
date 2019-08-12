from django.urls import path
from .views import *

app_name = 'qna'

urlpatterns = [
    path('', index, name='index'),
    path('/new/$', inquiry_add, name="inquiry_add"),
]