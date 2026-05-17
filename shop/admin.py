from django.contrib import admin

from .models import Category, Order, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    ordering = ['-id']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'stock')
    search_fields = ('title',)
    ordering = ['-id']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'product')
    search_fields = ('student__username', 'product__title')
    ordering = ['-id']
