from django import forms

import accounts.models
from shop.models import Product, Category, Sizes, Colors


class AddProductForm(forms.ModelForm):
    colors = Colors.objects.all().values_list('id', 'color_name')
    available_colours = forms.MultipleChoiceField(choices=colors, widget=forms.CheckboxSelectMultiple)
    sizes = Sizes.objects.all().values_list('id', 'size_name')
    available_sizes = forms.MultipleChoiceField(choices=sizes, widget=forms.CheckboxSelectMultiple)
    categories = Category.objects.all().values_list('id', 'name')
    category = forms.MultipleChoiceField(choices=categories, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Product
        fields = '__all__'


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AddressForm(forms.ModelForm):
    class Meta:
        model = accounts.models.Address
        # fields = '__all__'
        fields = ['country', 'city', 'address', 'zip']
        widgets = {
            'country': forms.Select,
            'city': forms.TextInput,
            'address': forms.TextInput,
            'zip': forms.TextInput
        }
