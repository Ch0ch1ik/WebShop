import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dashboard_get_no_login(client):
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_dashboard_get_login(client, user):
    url = reverse('dashboard')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_dashboard_get_with_permission(client, product, user_with_permission):
    url = reverse('dashboard')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_product_get_no_permission(client, user):
    url = reverse('add_product')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_product_get_with_permission(client, user_with_permission):
    url = reverse('add_product')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    from shop.forms import AddProductForm
    assert isinstance(form, AddProductForm)


@pytest.mark.django_db
def test_add_product_post_with_permission(client, user_with_permission, category, sizes, colors):
    url = reverse('add_product')
    client.force_login(user_with_permission)
    data = {
        'name': 'Spodnie Bum',
        'price': 10.50,
        'category': [1, 3],
        'description': 'opis produktu',
        'stock_quantity': 10,
        'available_sizes': [2],
        'available_colours': [3],
        'image': 'fake/test/url.png'
    }

    response = client.post(url, data)
    assert response.status_code == 302
    from shop.models import Product
    assert Product.objects.get(name='Spodnie Bum')
    assert response.url == reverse('show_products')


@pytest.mark.django_db
def test_add_category_get_no_permission(client, user):
    url = reverse('add_product')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_category_get_with_permission(client, user_with_permission):
    url = reverse('add_category')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    from shop.forms import AddCategoryForm
    assert isinstance(form, AddCategoryForm)


@pytest.mark.django_db
def test_add_category_post_with_permission(client, user_with_permission):
    url = reverse('add_category')
    client.force_login(user_with_permission)
    data = {
        'name': 'spodnie',
        'description': 'tararara'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    from shop.models import Category
    assert Category.objects.get(**data)
    assert response.url == reverse('show_categories')


@pytest.mark.django_db
def test_show_categories_get_no_permission(client, category, user):
    url = reverse('show_categories')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_show_categories_get_with_permission(client, category, user_with_permission):
    url = reverse('show_categories')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_category_get_no_permission(client, category, user):
    from shop.models import Category
    test_category = Category.objects.get(id=1)
    url = reverse('edit_category', kwargs={'pk': test_category.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_category_get_with_permission(client, category, user_with_permission):
    from shop.models import Category
    test_category = Category.objects.get(id=1)
    url = reverse('edit_category', kwargs={'pk': test_category.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_category_get_no_permission(client, category, user):
    from shop.models import Category
    test_category = Category.objects.get(id=1)
    url = reverse('delete_category', kwargs={'pk': test_category.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_category_get_with_permission(client, category, user_with_permission):
    from shop.models import Category
    test_category = Category.objects.get(id=1)
    url = reverse('delete_category', kwargs={'pk': test_category.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_category_post_with_permission(client, category, user_with_permission):
    client.force_login(user_with_permission)
    from shop.models import Category
    test_category = Category.objects.get(id=1)
    url = reverse('delete_category', kwargs={'pk': test_category.id})
    # url += "?next=" + reverse('show_categories')
    response = client.post(url, kwargs={'pk': test_category.id})
    assert response.status_code == 302
    assert response.url == reverse('show_categories')


@pytest.mark.django_db
def test_add_color_get_no_permission(client, user):
    url = reverse('add_colors')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_color_get_with_permission(client, user_with_permission):
    url = reverse('add_colors')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert form.is_valid


@pytest.mark.django_db
def test_add_color_post_with_permission(client, user_with_permission):
    url = reverse('add_colors')
    client.force_login(user_with_permission)
    data = {
        'color_name': 'zielony',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    from shop.models import Colors
    assert Colors.objects.get(**data)
    assert response.url == reverse('show_colors')


@pytest.mark.django_db
def test_edit_color_get_no_permission(client, colors, user):
    from shop.models import Colors
    test_color = Colors.objects.get(id=1)
    url = reverse('edit_color', kwargs={'pk': test_color.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_color_get_with_permission(client, colors, user_with_permission):
    from shop.models import Colors
    test_color = Colors.objects.get(id=1)
    url = reverse('edit_color', kwargs={'pk': test_color.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_size_get_no_permission(client, user):
    url = reverse('add_sizes')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_add_size_get_with_permission(client, user_with_permission):
    url = reverse('add_sizes')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert form.is_valid


@pytest.mark.django_db
def test_add_size_post_with_permission(client, user_with_permission):
    url = reverse('add_sizes')
    client.force_login(user_with_permission)
    data = {
        'size_name': 'XL',
    }
    response = client.post(url, data)
    assert response.status_code == 302
    from shop.models import Sizes
    assert Sizes.objects.get(**data)
    assert response.url == reverse('show_sizes')


@pytest.mark.django_db
def test_show_sizes_get_no_permission(client, sizes, user):
    url = reverse('show_sizes')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_show_sizes_get_with_permission(client, sizes, user_with_permission):
    url = reverse('show_sizes')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_size_get_no_permission(client, sizes, user):
    from shop.models import Sizes
    test_size = Sizes.objects.get(id=1)
    url = reverse('edit_size', kwargs={'pk': test_size.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_size_get_with_permission(client, sizes, user_with_permission):
    from shop.models import Sizes
    test_size = Sizes.objects.get(id=1)
    url = reverse('edit_size', kwargs={'pk': test_size.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_show_products_get_no_permission(client, product, user):
    url = reverse('show_products')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_show_products_get_with_permission(client, product, user_with_permission):
    url = reverse('show_products')
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_show_product_details_get_no_permission(client, product, user):
    from shop.models import Product
    test_product = Product.objects.get(id=1)
    url = reverse('product_details', kwargs={'pk': test_product.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_show_product_details_get_with_permission(client, product, user_with_permission):
    from shop.models import Product
    test_product = Product.objects.get(id=1)
    url = reverse('product_details', kwargs={'pk': test_product.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_edit_product_get_no_permission(client, product, user):
    from shop.models import Product
    test_product = Product.objects.get(id=1)
    url = reverse('edit_product', kwargs={'pk': test_product.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_product_get_with_permission(client, product, user_with_permission):
    from shop.models import Product
    test_product = Product.objects.get(id=1)
    url = reverse('edit_product', kwargs={'pk': test_product.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    from shop.forms import AddProductForm
    assert isinstance(form, AddProductForm)


@pytest.mark.django_db
def test_edit_product_post_with_permission(client, product, user_with_permission):
    url = reverse('edit_product')
    client.force_login(user_with_permission)
    data = {
        'name': 'koszulka Cyk',
        'price': 15.50,
        'category': '2',
        'description': 'opis produktu',
        'stock_quantity': 30,
        'available_sizes': '2',
        'available_colours': '3',
        'image': 'fake/test/url.png'
    }

    response = client.post(url, data)
    assert response.status_code == 302
    from shop.models import Product
    assert Product.objects.get(**data)
    assert response.url == reverse('show_products')


@pytest.mark.django_db
def test_delete_category_get_no_permission(client, colors, user):
    from shop.models import Colors
    test_color = Colors.objects.get(id=1)
    url = reverse('delete_color', kwargs={'pk': test_color.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_color_get_with_permission(client, colors, user_with_permission):
    from shop.models import Colors
    test_color = Colors.objects.get(id=1)
    url = reverse('delete_color', kwargs={'pk': test_color.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_color_post_with_permission(client, colors, user_with_permission):
    client.force_login(user_with_permission)
    from shop.models import Colors
    test_color = Colors.objects.get(id=1)
    url = reverse('delete_color', kwargs={'pk': test_color.id})
    response = client.post(url, kwargs={'pk': test_color.id})
    assert response.status_code == 302
    assert response.url == reverse('show_colors')


@pytest.mark.django_db
def test_delete_size_get_no_permission(client, sizes, user):
    from shop.models import Sizes
    test_size = Sizes.objects.get(id=1)
    url = reverse('delete_size', kwargs={'pk': test_size.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_size_get_with_permission(client, sizes, user_with_permission):
    from shop.models import Sizes
    test_size = Sizes.objects.get(id=1)
    url = reverse('delete_size', kwargs={'pk': test_size.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_size_post_with_permission(client, sizes, user_with_permission):
    client.force_login(user_with_permission)
    from shop.models import Sizes
    test_size = Sizes.objects.get(id=1)
    url = reverse('delete_size', kwargs={'pk': test_size.id})
    response = client.post(url, kwargs={'pk': test_size.id})
    assert response.status_code == 302
    assert response.url == reverse('show_sizes')


@pytest.mark.django_db
def test_delete_product_get_no_permission(client, product, user):
    from shop.models import Product
    test_product = Product.objects.get(id=1)
    url = reverse('delete_product', kwargs={'pk': test_product.id})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_product_get_with_permission(client, product, user_with_permission):
    from shop.models import Product
    test_product = Product.objects.get(id=1)
    url = reverse('delete_product', kwargs={'pk': test_product.id})
    client.force_login(user_with_permission)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_product_post_with_permission(client, product, user_with_permission):
    client.force_login(user_with_permission)
    from shop.models import Product
    test_product = Product.objects.get(id=1)
    url = reverse('delete_product', kwargs={'pk': test_product.id})
    response = client.post(url, kwargs={'pk': test_product.id})
    assert response.status_code == 302
    assert response.url == reverse('show_products')


@pytest.mark.django_db
def test_show_category_list_get_no_db(client):
    url = reverse('categories')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_show_category_list_get_with_db(client, category):
    url = reverse('categories')
    response = client.get(url)
    from shop.models import Category
    assert Category.objects.all()
    assert response.status_code == 200


@pytest.mark.django_db
def test_show_product_in_categories_get(client, category):
    url = reverse('products', kwargs={'pk': 1})
    response = client.get(url)
    assert response.status_code == 200
    from shop.models import Category
    assert Category.objects.all()


# @pytest.mark.django_db
# def test_show_product_in_categories_post():


@pytest.mark.django_db
def test_show_cart_get_no_db(client):
    url = reverse('cart')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_show_cart_get_db(client, cart, user):
    url = reverse('cart')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    from shop.models import Cart
    assert cart == Cart.objects.get(user_id=user.id)


@pytest.mark.django_db
def test_index_get(client, product):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_search_get(client):
    url = reverse('search')
    client.request('searchbox=tralala')
    url += "?" + 'search_box=tralala'
    response = client.get(url)
    assert response.status_code == 200


def test_index_post(client, product, user):
    url = reverse('add_category')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    from accounts.forms import LoginForm
    assert isinstance(form, LoginForm)


@pytest.mark.django_db
def test_create_order_view_get_not_logged(client):
    url = reverse('create_order')
    response = client.get(url)
    assert response.status_code == 302
    form = response.context['form']
    from shop.forms import AddressForm
    assert isinstance(form, AddressForm)


@pytest.mark.django_db
def test_create_order_view_get_logged(client, user, cart):
    url = reverse('create_order')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    from shop.forms import AddressForm
    assert isinstance(form, AddressForm)


@pytest.mark.django_db
def test_create_order_view_post_logged(client, user, cart):
    url = reverse('create_order')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    from shop.forms import AddressForm
    assert isinstance(form, AddressForm)
    from accounts.models import Address
    assert Address.objects.get(user=user)


def test_my_account_view_not_login(client):
    url = reverse('my_account')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_my_account_view_not_login(client, user):
    client.force_login(user)
    url = reverse('my_account')
    response = client.get(url)
    assert response.status_code == 200
