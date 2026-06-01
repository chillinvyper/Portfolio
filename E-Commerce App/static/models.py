from django.db import models
from decimal import Decimal
from django.urls import reverse
from django.conf import settings


# Create your models here.
# creating User model
class UserProfile(models.Model):
    '''Creating the User model, with dwdicated roles, and poperty checks
    for with role the current user is, as well as string returns for
    username and role'''

    # set selectable roles
    VENDOR = 'vendor'
    SHOPPER = 'shopper'
    ROLE_CHOICES = [(VENDOR, 'vendor'), (SHOPPER, 'shopper')]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        )

    # sets the choices for groups available to the user
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # a string return for the username and role of the user
    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

    # user the property decorator on the role check functions
    @property
    def is_vendor(self):
        '''boolean check for role'''
        return self.role == self.VENDOR

    @property
    def is_shopper(self):
        '''boolean check for role'''
        return self.role == self.SHOPPER


# creating the Store model
class Store(models.Model):
    '''creating the Store model, with a foreign key to the User model.
    The required information for the model is: owner(foreign key), description,
    name and  DateTime of creation'''

    # set the owner as a foreign key
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='stores')

    # set the remaining characteristics
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # setting the Meta subclass
    class Meta:
        ordering = ['name']

    # create the string return function
    def __str__(self):
        return f'{self.name}'

    # create the function to return the absolute URL, using primary key
    def get_absolute_url(self):
        return reverse('store_detail', kwargs={'pk': self.pk})


# creating the Product model
class Product(models.Model):
    '''creating the Product model, with a foreign key to the Store model.
    The required information is: store(foregin key), name, description,
    price, stock level and DateTime of creation'''

    # create the store foreign key
    store = models.ForeignKey(Store, on_delete=models.CASCADE,
                              related_name='products')

    # set remaining characteristics
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    # creating the Meta subclass
    class Meta:
        ordering = ['name']

    # creating string return function
    def __str__(self):
        return f'{self.name} - {self.store.name}'

    # creating function to return absolute URL
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})

    # using the property decorator to return the decimal price value
    @property
    def display_price(self):
        return Decimal(self.price)
