"""WebShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from django.views.generic import TemplateView
from accounts import views as acc_views
from shop import views as shop_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', shop_views.IndexView.as_view(), name='index'),
    path('login/', acc_views.LoginView.as_view(), name='login'),
    path('logout/', acc_views.LogoutView.as_view(), name='logout'),
    path('create_user/', acc_views.RegisterView.as_view(), name='add_user'),
    path('add_category/', shop_views.AddCategoryView.as_view(), name='add_category'),
    path('show_categories/', shop_views.ShowCategoriesView.as_view(), name='show_categories'),
    path('edit_category/<int:pk>/', shop_views.CategoryUpdateView.as_view(), name='edit_category'),
    path('delete_category/<int:pk>/', shop_views.CategoryDeleteView.as_view(), name='delete_category'),
    path('add_product/', shop_views.AddProductView.as_view(), name='add_product'),
    path('show_products/', shop_views.ShowProductsView.as_view(), name='show_products'),
    path('product_detail/<int:pk>/', shop_views.ProductDetailsView.as_view(), name='product_details'),
    path('edit_product/<int:pk>/', shop_views.ProductUpdateView.as_view(), name='edit_product'),
    path('delete_product/<int:pk>/', shop_views.ProductDeleteView.as_view(), name='delete_product'),
    path('colors/', shop_views.ShowColorsView.as_view(), name='show_colors'),
    path('edit_color/<int:pk>/', shop_views.ColorsUpdateView.as_view(), name='edit_color'),
    path('delete_color/<int:pk>/', shop_views.ColorDeleteView.as_view(), name='delete_color'),
    path('show_sizes/', shop_views.ShowSizesView.as_view(), name='show_sizes'),
    path('add_colors/', shop_views.AddColorsView.as_view(), name='add_colors'),
    path('add_sizes/', shop_views.AddSizesView.as_view(), name='add_sizes'),
    path('edit_size/<int:pk>/', shop_views.SizeUpdateView.as_view(), name='edit_size'),
    path('delete_size/<int:pk>/', shop_views.SizeDeleteView.as_view(), name='delete_size'),
    path('dashboard/', shop_views.DashboardView.as_view(), name='dashboard'),
    path('categories/', shop_views.CategoriesView.as_view(), name='categories'),
    path('products/<int:pk>/', shop_views.CategoryProductsView.as_view(), name='products'),
    path('cart/', shop_views.CartView.as_view(), name='cart'),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
