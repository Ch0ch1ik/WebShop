from random import Random

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=240)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('edit_category', args=(self.id,))


class Sizes(models.Model):
    size_name = models.CharField(max_length=25)

    def __str__(self):
        return self.size_name

    def get_absolute_url(self):
        return reverse('edit_size', args=(self.id,))


class Colors(models.Model):
    color_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.color_name

    def get_absolute_url(self):
        return reverse('edit_color', args=(self.id,))


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.FloatField()
    category = models.ManyToManyField(Category)
    description = models.TextField()
    stock_quantity = models.IntegerField(default=0)
    available_sizes = models.ManyToManyField(Sizes)
    available_colours = models.ManyToManyField(Colors)
    image = models.ImageField(upload_to='shop/media/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_details', args=(self.id,))

    def get_edit_url(self):
        return reverse('edit_product', args=(self.id,))


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductInCart')
    amount = models.FloatField(null=True)


class ProductInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField()
    product_color = models.ForeignKey(Colors, on_delete=models.CASCADE)
    product_size = models.ForeignKey(Sizes, on_delete=models.CASCADE)


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
