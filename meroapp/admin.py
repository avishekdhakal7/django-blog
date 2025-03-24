from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','image','date','description','price']

# Register your models here.
