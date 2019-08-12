from django.db import models

# Create your models here.
class Inquiry(models.Model) :
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    product = models.CharField(max_length=200)
    title = models.CharField(max_length=200, default="문의")
    content = models.TextField()
    image = models.ImageField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)