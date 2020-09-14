from django.contrib import admin
from django.contrib.admin import AdminSite, ModelAdmin
from django.forms import models

from records.models import User, Order, Product

AdminSite.site_title = "Laikipia Wines And Spirits"
AdminSite.site_header = 'Laikipia Wines And Spirits'
admin.site.register(User)


class ProductAdmin(ModelAdmin):
    list_display = ['title', 'description', 'size', 'current_stock', 'current_price', 'old_price', 'date_added']


class OrderAdmin(ModelAdmin):
    list_display = ["product", "user", "then_price", "amount", "date_purchased"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
# Register your models here.
