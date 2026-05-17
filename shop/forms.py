from django import forms

from .models import Category, Order, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'price', 'image', 'stock']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'product']
