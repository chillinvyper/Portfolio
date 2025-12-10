from django.urls import path
from . import views


urlpatterns = [
    # Home / Stores
    path("", views.home, name='home'),
    path('stores/', views.store_list, name='store_list'),
    path('store/<int:pk>/', views.store_detail, name='store_detail'),

    # Vendor store management
    path('store/create/', views.store_create, name='store_create'),
    path('store/<int:store_id>/edit/', views.store_edit, name='store_edit'),
    path('store/<int:store_id>/delete/', views.store_delete, name='store_delete'),

    # Products
    path('store/<int:pk>/product/add/', views.product_create, name='product_create'),
    path('product/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('store/<int:store_id>/product/<int:product_id>/', views.product_detail,
         name='product_detail'),

    # Basket & checkout
    path('basket/', views.basket_view, name='basket'),
    path('basket/add/<int:product_id>/', views.basket_add, name='basket_add'),
    path('basket/remove/<int:item_id>/', views.basket_remove, name='basket_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<int:order_id>/', views.checkout_success, name='checkout_success'),

    # Orders (shopper & vendor)
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('vendor/orders/', views.vendor_orders, name='vendor_orders'),

    # Authentication & registration
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logged_out', views.logout_user, name='logout_user'),
    ]
