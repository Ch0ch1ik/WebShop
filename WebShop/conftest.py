import pytest
from django.contrib.auth.models import User, Permission

from shop.models import Category, Sizes, Colors, Product, Cart


@pytest.fixture
def user():
    data = {
        'username': 'testowy',
        'password': 'testowy'
    }
    return User.objects.create_user(**data)


@pytest.fixture
def user_login():
    data = {
        'username': 'testowy',
        'password': 'testowy'
    }
    User.objects.create_user(**data)
    return data


@pytest.fixture()
def category():
    lst = []
    cat = Category.objects.create(id=1, name='ubrania', description='Opis jest bez sensu')
    lst.append(cat)
    cat2 = Category.objects.create(id=2, name='damskie', description='Opis', parent=cat)
    lst.append(cat2)
    cat3 = Category.objects.create(id=3, name='spodnie', description='Opis jest', parent=cat2)
    lst.append(cat3)
    return lst


@pytest.fixture()
def sizes():
    lst = [
        Sizes.objects.create(id=1, size_name='L'),
        Sizes.objects.create(id=2, size_name='S'),
        Sizes.objects.create(id=3, size_name='M'),
    ]
    return lst


@pytest.fixture()
def colors():
    lst = [
        Colors.objects.create(id=1, color_name='zielony'),
        Colors.objects.create(id=2, color_name='czerwony'),
        Colors.objects.create(id=3, color_name='zolty'),
    ]
    return lst


@pytest.fixture()
def product(category, sizes, colors):
    lst = []
    for x in range(10):
        p = Product()
        p.id = x
        p.name = 'Spodnie Bum' + str(x)
        p.price = 10.0 + x
        p.save()
        p.category.set(category, through_defaults={'name': 'spodnie'})
        p.description = 'Opis produktu'
        p.stock_quantity = 10 + x
        p.available_sizes.set(sizes, through_defaults={'size_name': 'M'})
        p.available_colours.set(colors, through_defaults={'color_name': 'zolty'})
        p.image = 'fake/test/url.png'
        p.save()
        lst.append(p)
    return lst


@pytest.fixture()
def user_with_permission():
    data = {
        'username': 'testowy',
        'password': 'alamakota',
    }
    u = User.objects.create_user(**data)
    p = Permission.objects.get(codename='add_product')
    p1 = Permission.objects.get(codename='add_category')
    p2 = Permission.objects.get(codename='view_category')
    p3 = Permission.objects.get(codename='change_category')
    p4 = Permission.objects.get(codename='delete_category')
    p5 = Permission.objects.get(codename='add_colors')
    p6 = Permission.objects.get(codename='change_colors')
    p7 = Permission.objects.get(codename='add_sizes')
    p8 = Permission.objects.get(codename='view_sizes')
    p9 = Permission.objects.get(codename='change_sizes')
    p10 = Permission.objects.get(codename='view_product')
    p11 = Permission.objects.get(codename='change_product')
    p12 = Permission.objects.get(codename='delete_colors')
    p13 = Permission.objects.get(codename='delete_sizes')
    p14 = Permission.objects.get(codename='delete_product')
    u.user_permissions.add(p, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14)
    return u


@pytest.fixture()
def cart(user):
    return Cart.objects.create(id=1, user=user)

