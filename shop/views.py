import random
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView, FormView
from accounts.forms import LoginForm
from accounts.models import Address
from shop.forms import AddProductForm, AddCategoryForm, AddressForm
from shop.models import Category, Product, Colors, Sizes, Cart, ProductInCart, Order


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, 'dashboard.html')


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
    permission_required = ['shop.view_category']
    model = Category
    fields = '__all__'
    template_name = 'categories_list.html'


class CategoryUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['shop.change_category']
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
    permission_required = ['shop.change_colors']
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
    permission_required = ['shop.change_sizes']
    model = Sizes
    template_name = 'add_object.html'
    fields = '__all__'

    def get_success_url(self):
        super().get_success_url()
        return reverse("show_sizes")


class ShowProductsView(PermissionRequiredMixin, ListView):
    permission_required = ['shop.view_product']
    model = Product
    template_name = 'products_list.html'


class ProductDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = ['shop.view_product']
    model = Product
    template_name = 'product_details.html'


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ['shop.change_product']
    model = Product
    template_name = 'add_object.html'
    form_class = AddProductForm

    def get_success_url(self):
        super().get_success_url()
        return reverse("show_products")


class ColorDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['shop.delete_colors']
    model = Colors
    success_url = reverse_lazy('show_colors')
    template_name = 'confirm_delete.html'


class SizeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ['shop.delete_sizes']
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
        products = Product.objects.filter(category=category)
        return products

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=request.POST.get('id'))
        color = Colors.objects.get(color_name=request.POST.get('color'))
        size = Sizes.objects.get(size_name=request.POST.get('size'))
        chosen_amount = int(request.POST.get('amount'))

        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, made_order=False)
            # cart.save()
            product_in_cart = ProductInCart.objects.create(product=product, cart=cart,
                                                           amount=chosen_amount,
                                                           product_size=size, product_color=color)

            cart.productincart_set.all()
            cart.save()
            return redirect('cart')

        else:
            return render(request, 'login.html', {'form': LoginForm()})


class CartView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user, made_order=False)
            products_in_cart = ProductInCart.objects.all().filter(cart_id=cart.id)
            total_sum = 0
            for product in products_in_cart:
                total_sum += product.get_sum
            return render(request, 'cart.html', {'products': products_in_cart, 'total_sum': total_sum})

    def post(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, made_order=False)
        products_in_cart = ProductInCart.objects.all().filter(cart_id=cart.id)
        total_sum = 0
        for product in products_in_cart:
            amount_up = request.POST.get('up' + str(product.id))
            amount_down = request.POST.get('down' + str(product.id))
            print(product.id)
            print(product.amount)
            if product.amount >= 1:
                if amount_up:
                    product.amount += 1
                    product.save()
                elif amount_down:
                    product.amount -= 1
                    product.save()
                    if product.amount == 0:
                        product.delete()
            else:
                pass
            total_sum += product.get_sum
        return render(request, 'cart.html', {'products': products_in_cart, 'total_sum': total_sum})


class IndexView(View):
    def get(self, request):
        products = list(Product.objects.all())
        products = random.sample(products, 3)
        return render(request, 'index.html', {'products': products})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('id'))
            color = Colors.objects.get(color_name=request.POST.get('color'))
            size = Sizes.objects.get(size_name=request.POST.get('size'))
            chosen_amount = int(request.POST.get('amount'))

            cart, created = Cart.objects.get_or_create(user=request.user, made_order=False)
            product_in_cart = ProductInCart.objects.create(product=product, cart=cart,
                                                           amount=chosen_amount,
                                                           product_size=size, product_color=color)
            cart.productincart_set.all()
            cart.save()
            return redirect('cart')

        else:
            return redirect('login')


class ProductCardView(DetailView):
    model = Product
    template_name = 'product_card.html'


class SearchView(View):
    def get(self, request):
        data = self.request.GET['search_box']
        search_in_name = Product.objects.filter(name__icontains=data)
        search_in_description = Product.objects.filter(description__icontains=data)
        products = search_in_name.union(search_in_description).order_by('name')
        return render(request, 'products.html', {'products': products})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = Product.objects.get(id=request.POST.get('id'))
            color = Colors.objects.get(color_name=request.POST.get('color'))
            size = Sizes.objects.get(size_name=request.POST.get('size'))
            chosen_amount = int(request.POST.get('amount'))

            cart, created = Cart.objects.get_or_create(user=request.user, made_order=False)
            product_in_cart = ProductInCart.objects.create(product=product, cart=cart,
                                                           amount=chosen_amount,
                                                           product_size=size, product_color=color)
            cart.productincart_set.all()
            cart.save()
            return redirect('cart')

        else:
            return redirect('login')


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        address, created = Address.objects.get_or_create(user=request.user)
        form = AddressForm(instance=address)
        cart = Cart.objects.get(user=request.user, made_order=False)
        products_in_cart = ProductInCart.objects.all().filter(cart_id=cart.id)
        total_sum = 0
        for product in products_in_cart:
            total_sum += product.get_sum
        return render(request, 'create_order.html',
                      {'form': form, 'products_in_cart': products_in_cart, 'total_sum': total_sum, 'cart_id': cart.id})

    def post(self, request):
        address = Address.objects.create(user=request.user)
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.country = request.POST.get('country')
        address.zip = request.POST.get('zip')
        address.save()
        cart = Cart.objects.get(user=request.user, made_order=False)
        order = Order.objects.create(cart_id=cart.id, address_id=address.id, creator=request.user)
        order.save()
        cart.made_order = True
        cart.save()
        return redirect('my_account')


class MyAccountView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            orders = Order.objects.all().filter(creator=request.user)
            return render(request, 'my_account.html', {'orders': orders})


class MyTest(View):
    def get(self, request):
        return render(request, 'my_test.html')
