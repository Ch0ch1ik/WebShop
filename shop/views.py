from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, FormView

from shop.forms import AddProductForm
from shop.models import Category, Product, Colors, Sizes


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'dashboard.html')


class AddProductView(PermissionRequiredMixin, View):
    permission_required = ['shop.add_product']

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        form = AddProductForm()
        return render(request, 'add_object.html', {'form': form})

    def post(self, request):
        form = AddProductForm(request.POST)
        if form.is_valid():
            Product.objects.create(**form.cleaned_data)
            form = AddProductForm()
        return render(request, 'add_object.html', {'form': form})


# Create your views here.
class AddCategoryView(PermissionRequiredMixin, CreateView):
    permission_required = ['shop.add_category']
    model = Category
    template_name = 'add_object.html'
    fields = '__all__'
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
        return reverse("edit_category")


class CategoryDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['shop.delete_category']
    model = Category
    success_url = reverse_lazy('show_categories')
    template_name = 'category_confirm_delete.html'


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
