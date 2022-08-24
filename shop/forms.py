from django import forms

from shop.models import Product, Category


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
