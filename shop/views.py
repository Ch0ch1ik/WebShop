import random
from random import randint

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.forms import MultipleChoiceField, CheckboxSelectMultiple
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, FormView

import accounts
from accounts.forms import LoginForm
from shop.forms import AddProductForm, AddCategoryForm
from shop.models import Category, Product, Colors, Sizes, Cart, ProductInCart


class DashboardView(LoginRequiredMixin, View):

    def get(self, request):
        cart = Cart.objects.get(user_id=self.request.user)
        cart_id = cart.id
        return render(request, 'dashboard.html', {'cart': cart_id})

    # @property
    # def get_cart_id(self):
    #     user_cart = Cart.objects.get(user_id=self.request.user)
    #     return user_cart.id


class AddProductView(PermissionRequiredMixin, CreateView):
    permission_required = ['shop.add_product']
    form_class = AddProductForm
    template_name = 'add_object.html'
    success_url = reverse_lazy('show_products')


class AddCategoryView(PermissionRequiredMixin, CreateView):
    permission_required = ['shop.add_category']
    form_class = AddCategoryForm
    template_name = 'add_object.html'
    success_url = reverse_lazy('show_categories')


class ShowCategoriesView(PermissionRequiredMixin, ListView):
    permission_required = ['shop.view_categories']
    model = Category
    fields = '__all__'
    template_name = 'categories_list.html'


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['shop.edit_category']
    model = Category
    template_name = 'add_object.html'
    fields = '__all__'

    def get_success_url(self):
        super().get_success_url()
        return reverse("show_categories")


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['shop.delete_category']
    model = Category
    success_url = reverse_lazy('show_categories')
    template_name = 'confirm_delete.html'


class AddColorsView(PermissionRequiredMixin, CreateView):
    permission_required = ['shop.add_colors']
    model = Colors
    template_name = 'add_object.html'
    fields = '__all__'
    success_url = reverse_lazy('show_colors')


class ColorsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['shop.edit_color']
    model = Colors
    template_name = 'add_object.html'
    fields = '__all__'

    def get_success_url(self):
        super().get_success_url()
        return reverse("show_colors")


class AddSizesView(PermissionRequiredMixin, CreateView):
    permission_required = ['shop.add_sizes']
    model = Sizes
    template_name = 'add_object.html'
    fields = '__all__'
    success_url = reverse_lazy('show_sizes')


class ShowColorsView(PermissionRequiredMixin, ListView):
    permission_required = ['shop.view_colors']
    model = Colors
    template_name = 'colors_list.html'


class ShowSizesView(PermissionRequiredMixin, ListView):
    permission_required = ['shop.view_sizes']
    model = Sizes
    template_name = 'sizes_list.html'


class SizeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['shop.edit_size']
    model = Sizes
    template_name = 'add_object.html'
    fields = '__all__'

    def get_success_url(self):
        super().get_success_url()
        return reverse("show_sizes")


class ShowProductsView(PermissionRequiredMixin, ListView):
    permission_required = ['shop.view_products']
    model = Product
    template_name = 'products_list.html'


class ProductDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = ['shop.view_details']
    model = Product
    template_name = 'product_details.html'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['shop.edit_product']
    model = Product
    template_name = 'add_object.html'
    form_class = AddProductForm

    def get_success_url(self):
        super().get_success_url()
        return reverse("show_products")


class ColorDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['shop.delete_color']
    model = Colors
    success_url = reverse_lazy('show_colors')
    template_name = 'confirm_delete.html'


class SizeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['shop.delete_size']
    model = Sizes
    success_url = reverse_lazy('show_sizes')
    template_name = 'confirm_delete.html'


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['shop.delete_product']
    model = Product
    success_url = reverse_lazy('show_products')
    template_name = 'confirm_delete.html'


class CategoriesView(ListView):
    model = Category
    template_name = 'categories.html'


class CategoryProductsView(ListView):
    model = Product
    template_name = 'products.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        category = Category.objects.get(pk=pk)
        return Product.objects.all().filter(category=category)

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.POST.get('id'))
        color = Colors.objects.get(color_name=request.POST.get('color'))
        size = Sizes.objects.get(size_name=request.POST.get('size'))
        chosen_amount = int(request.POST.get('amount'))

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            # cart.save()
            product_in_cart = ProductInCart.objects.create(product=product, cart=cart,
                                                           amount=chosen_amount,
                                                           product_size=size, product_color=color)

            cart.productincart_set.all()
            cart.save()
            return redirect('cart')

        else:
            return render(request, 'login.html', {'form': LoginForm()})


class CartView(View):

    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            products_in_cart = ProductInCart.objects.all().filter(cart_id=cart.id)
            return render(request, 'cart.html', {'products': products_in_cart})
        else:
            return render(request, 'login.html', {'form': LoginForm()})


class IndexView(View):
    def get(self, request):
        products = list(Product.objects.all())
        products = random.sample(products, 3)
        return render(request, 'index.html', {'products': products})


