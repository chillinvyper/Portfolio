from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Store, Product

# create the form to create a new user
class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)
    email = forms.EmailField(required=True)

    class Meta:
        # set the base model using the models created in the .models file
        model = User

        # create the fields for the form
        fields = [
            'username',
            'email',
            'role',
            'password1',
            'password2'
        ]


# create form for a new store
class StoreForm(forms.ModelForm):

    class Meta:
        # set the base model using the models created in the .models file
        model = Store

        # create the fields for the form
        fields = ['name', 'description']


# create the form for a new product
class ProductForm(forms.ModelForm):

    class Meta:
        # set the base model using the models created in the .models file
        model = Product

        # create the fields for the form
        fields = [
            'store',
            'name',
            'description',
            'price',
            'stock'
        ]

    # creating a function to ensure that vendors can only access their
    # own products
    def __init__(self, *args, **kwargs):

        # removes the vendor from the kwargs dictionary and returns it,
        # or returns None, which is handled later on
        vendor = kwargs.pop('vendor', None)

        # forces djangos normal for setup to allow for self.fields
        super().__init__(*args, **kwargs)

        # checks there is a vendor
        if vendor is not None:

            # access the store fields as a dictionary, displaying only
            # the ones related to that vendor
            self.fields['store'].queryset = Store.objects.filter(owner=vendor)
