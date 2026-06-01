from django.urls import path
from . import views as v

urlpatterns = [
    # url paths for the main page, signup and home dashboard pages
    path('', v.home, name='home'),
    path('signup/', v.signup, name='signup'),
    path('dashboard/', v.vendor_dashboard, name='vendor_dashboard'),

    # url paths for the store pages
    path('stores/<int:pk>/', v.store_detail, name='store_detail'),
    path('stores/new/', v.store_create, name='store_create'),
    path('stores/<int:pk>/edit', v.store_update, name='store_update'),
    path('stores/<int:pk>/delete/', v.store_delete, name='store_delete'),

    # url paths for the product pages
    path('products/<int:pk>/', v.product_detail, name='product_detail'),
    path('products/new/', v.product_create, name='product_create'),
    path('products/<int:pk>/edit/', v.product_update, name='product_update'),
    path('product/<int:pk>/delete/', v.product_delete, name='product_delete'),

    # url paths for the basket pages
    path('basket/', v.basket_detail, name='basket_detail'),
    path('basket/add/<int:product_id>/', v.basket_add, name='basket_add'),
    path('basket/remove/<int:product_id>/', v.basket_remove, name='basket_remove'),

    # url path for the checkout
    path('checkout/', v.checkout, name='checkout')
]
