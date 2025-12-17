from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    VENDOR = 'vendor'
    SHOPPER = 'shopper'
    ROLE_CHOICES = [(VENDOR, 'Vendor'), (SHOPPER, 'Shopper')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=SHOPPER)

    def is_vendor(self):
        return self.role == self.VENDOR

    def is_shopper(self):
        return self.role == self.SHOPPER


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=False, blank=True)

    class Meta:
        unique_together = ('owner', 'slug')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('store_detail', args=[self.id])


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.store.name})"


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')

    def get_total_price(self):
        return sum(item.line_total() for item in self.user.basket_items.all())


class BasketItem(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='basket_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)


class Meta:
    unique_together = ('user', 'product')


def line_total(self):
    return self.quantity * self.product.price


class Order(models.Model):
    shopper = models.ForeignKey('User', on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
