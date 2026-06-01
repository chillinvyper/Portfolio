from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.http import HttpResponseForbidden
from .forms import SignUpForm, StoreForm, ProductForm
from .models import UserProfile, Store, Product

# Create your views here.


# =============================ROLE CHECKS==============================
def get_user_role(user):
    '''a helper fucntion to check if the User profile exists,
    and return its role'''
    if not user.is_authenticated:
        return None
    try:
        return user.userprofile.role
    except UserProfile.DoesNotExist:
        return None


def is_vendor(user):
    '''A function to check if the user is a vendor, using the helper
    function to retrieve the role'''
    return get_user_role(user) == UserProfile.VENDOR


def is_shopper(user):
    '''A function to check if the user is a shopper, using the helper
    function to retrieve the role'''
    return get_user_role(user) == UserProfile.SHOPPER


# ========================CUSTOM DECORATORS=============================
def vendor_required(view_func):
    '''creating a decorator function to ensure the user is logged in and
    is a Vendor'''

    # uses args and kwargs to ensure the fuction runs regardless of the
    # amount of arguments passed
    def wrapper(request, *args, **kwargs):
        '''Checks if the user making the http request is authenticated
        and has the correct role'''

        # checks whether the user is logged in
        if not request.user.is_authenticated:

            # returns them to the login page if not logged in
            return redirect('login')

        # users helper function to check if user is not a shopper
        if not is_vendor(request.user):
            return HttpResponseForbidden('Only Vendors can access this page')

        # only returns if the user is logged in and is a vendor
        return view_func(request, *args, **kwargs)

    # returns the wrapper function
    return wrapper


def shopper_required(view_func):
    '''creating a decorator function to ensure the user is logged in and
    is a Shopper'''

    # uses args and kwargs to ensure the fuction runs regardless of the
    # amount of arguments passed
    def wrapper(request, *args, **kwargs):

        # checks if the user is logged in
        if not request.user.is_authenticated:

            # return the user to the login page if they are not logged in
            return redirect('login')

        # checks if they are not a shopper using the helper function
        if not is_shopper(request.user):

            # forbids the user if they are not a shopper
            return HttpResponseForbidden('Only Shoppers can access this page')

        # returns the function after the checks
        return view_func(request, *args, **kwargs)

    # returns the result of the wrapper
    return wrapper


# ===========================HOME PAGE & SIGN UP PAGES==================
def home(request):
    '''loads the home page using a prefetched query set to retrieve all
    of the stores and their products'''
    stores = Store.objects.prefetch_related('products').all()
    return render(request, 'shop/home.html', {'stores': stores})


def signup(request):
    '''the function that allows for the creation of a new user and to display
    the form.'''
    if request.method == 'POST':

        # assigns the completed for if it recieves a POST request
        form = SignUpForm(request.POST)

        # checks the form is valid against the built in checks
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
            login(request, user)
            messages.success(request, 'Account successfully created.')
            return redirect('home')
    else:
        # handles the initial GET request
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})


# ==========================STORE SPECIFIC==============================
# ensures the user is logged in and is a vendor using the earlier
# created decorator
@login_required
@vendor_required
def vendor_dashboard(request):
    '''displays only stores where the user is the owner and prefetches
    all the related products'''
    stores = Store.objects.filter(owner=request.user).prefetch_related(
        'products')
    return render(request, 'shop/dashboard.html', {'stores': stores})


def store_detail(request, pk):
    '''displays the stores products using a prefetch to get all products
    at once using the primary key of the store'''
    store = get_object_or_404(Store.objects.prefetch_related('products'), pk=pk)
    return render(request, 'shop/store_detail.html', {'store': store})


# ensures the user is a vendor and logged in by using decorators
@login_required
@vendor_required
def store_create(request):
    '''Allows for the creation of a new store if the user is a vendor,
    and auto-assigns them as the owner'''

    # check the form is valid against the inbuilt checks
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            messages.success(request, 'Store created successfully.')
            return redirect(store)
    else:
        # handles the initial GET request
        form = StoreForm()

    # renders the blank store creation form
    return render(
        request, 'shop/store_form.html', {
            'form': form, 'title': 'Create Store'
            }
        )


# uses decorators to ensure the user is logged and a vendor
@login_required
@vendor_required
def store_update(request, pk):

    # retrieves the store requested using its primary key
    store = get_object_or_404(Store, pk=pk, owner=request.user)
    if request.method == 'POST':

        # displaysd the form with the current details prefilled
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store details Updated successfully.')
            return redirect(store)
    else:

        # displays the form prefilled with current details for the initial GET request
        form = StoreForm(instance=store)
    return render(
        request, 'shop/store_form.html', {
            'form': form, 'title': 'Edit Store'
            }
        )


# uses decorators to ensure the user is logged and a vendor
@login_required
@vendor_required
def store_delete(request, pk):

    # gets the correct store using the sotres primary key
    store = get_object_or_404(Store, pk=pk, owner=request.user)
    if request.method == 'POST':

        # deletes the store from the database
        store.delete()
        messages.success(request, 'Store successfullly deleted.')
        return redirect('vendor_dashboard')
    return render(request, 'shop/store_confirm_delete.html', {'store': store})


# ==============================PRODUCT SPECIFIC========================
def product_detail(request, pk):
    '''gets and displays the requested product using its primary key and
      a select_related search to narrow the search down to the store it
      is from'''

    product = get_object_or_404(Product.objects.select_related('store'), pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


# uses decorators to ensure the user is logged and a vendor
@login_required
@vendor_required
def product_create(request):
    '''The view for the display and useage of the product creation form'''

    if request.method == 'POST':
        form = ProductForm(request.POST, vendor=request.user)
        if form.is_valid():
            product = form.save(commit=False)

            # checks if the requesting user is the store owner
            if product.store.owner != request.user:
                return HttpResponseForbidden("You can't add products to this store")

            # if the check is passed, only then is the product saved
            product.save()
            messages.success(request, 'Product created successfully')
            return redirect(product)
    else:
        # handles the initial GET request
        form = ProductForm(vendor=request.user)
    return render(
        request, 'shop/product_form.html', {
            'form': form, 'title': 'Create Product'
            }
        )


# using decorators to ensure the user is logged in and is a vendor
@login_required
@vendor_required
def product_update(request, pk):
    '''Allows the editing of the product details, price, name and quantity
    whilst ensuring only the store owner can edit the store'''
    product = get_object_or_404(
        Product.objects.select_related('store'),
        pk=pk, store__owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product, vendor=request.user)
        if form.is_valid():

            # creates an updated version of the product based on the new form
            updated_product = form.save(commit=False)

            # checks if the request user is the owner of the store the
            # product is in
            if updated_product.store.owner != request.user:
                return HttpResponseForbidden(
                    'You cannot edit another vendors product.')
            updated_product.save()
            messages.success(request, 'Product has been updated.')
            return redirect(updated_product)
    else:
        # handles the initial GET request
        form = ProductForm(instance=product, vendor=request.user)
    return render(
        request, 'shop/product_form.html', {
            'form': form, 'title': 'Edit Product'
            }
        )


# using decorators to ensure the user is logged in and is a vendor
@login_required
@vendor_required
def product_delete(request, pk):
    '''allows for the deletion of a product, following a confirmation
    selection'''
    # Retrieves product, checking if the request user is the product owner
    product = get_object_or_404(Product, pk=pk, store__owner=request.user)
    if request.method == 'POST':
        # deletes the product
        product.delete()
        # displays a success response
        messages.success(request, 'Products successfully deleted.')
        # returns the user to the dashboard
        return redirect('vendor_dashboard')
    return render(
        request, 'shop/product_confirm_delete.html', {
            'product': product
            }
        )


# ==========================BASKET SPECIFIC=============================
def get_basket(request):
    '''returns the current basket contents'''
    return request.session.setdefault('basket', {})


def save_basket(request, basket):
    '''allows the user to leave the page and returnn to the basket
    without losing their items in the basket'''
    request.session['basket'] = basket
    request.session.modified = True


def basket_items_and_total(basket):
    '''a helper fuction to calculate the totals for the items in the basket
    and the grand total'''
    product_ids = basket.keys()
    products = Product.objects.filter(id__in=product_ids).select_related('store')
    # creates an empty list for the items
    items = []
    # establishes a total variable to handle decimels
    total = Decimal('0.00')
    # iterates through the items in the basket to calculate the total
    for product in products:
        quantity = int(basket[str(product.id)])
        # calculates the total for each item
        line_total = product.price * quantity
        # adds the line total to the grand total
        total += line_total
        # adds the current item to the list for the checkout and invoice
        items.append(
            {
                'product': product,
                'quantity': quantity,
                'line_total': line_total
            }
        )
    return items, total


# using decoraters to check the user is logged in as a shopper
@login_required
@shopper_required
def basket_add(request, product_id):
    ''' checks whether the porduct has enough stock before adding it to
    the current session basket'''
    product = get_object_or_404(Product, pk=product_id)

    # checks product isnt out of stock
    if product.stock <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect(product)

    # uses helper fucntion to get the current session basket
    basket = get_basket(request)
    current_quantity = int(basket.get(str(product.id), 0))

    # checks the requested quantity isnt greater than the current stock level
    if current_quantity >= product.stock:
        messages.error(request, "You can't order more than the available stock")
        return redirect(product)
    # adds the product to the basket or increases its quantity
    basket[str(product.id)] = current_quantity + 1
    save_basket(request, basket)
    messages.success(request, f'Added {product.name} to your basket.')
    return redirect('basket_detail')


# uses decorators to ensure user is logged in as a shopper
@login_required
@shopper_required
def basket_remove(request, product_id):
    '''allows a product to be removed from the session basket'''
    basket = get_basket(request)
    product_key = str(product_id)
    if product_key in basket:
        del basket[product_key]
        save_basket(request, basket)
        messages.success(request, 'Item removed successfully.')
    return redirect('basket_detail')


# uses decorators to ensure user is logged in as a shopper
@login_required
@shopper_required
def basket_detail(request):
    '''returns a dictionary to display the contents of the basket using the
    helper functions to do the calculations'''
    basket = get_basket(request)
    items, total = basket_items_and_total(basket)
    return render(
        request,
        'shop/basket.html',
        {
            'items': items,
            'total': total
        },
    )


# ============================CHECKOUT==================================
# uses decorators to ensure user is logged in as a shopper
@login_required
@shopper_required
def checkout(request):
    '''The final checkout function, allowing the totals to be created, the
    invoice to be generated and emailed to the users saved email address,
    it is currently set to display in the terminal for testing purposes'''
    basket = get_basket(request)
    items, total = basket_items_and_total(basket)

    # displays a message if the basket is empty
    if not items:
        messages.error(request, 'Your basket contains no items.')
        return redirect('basket_detail')

    # builds the invoice to be sent to the users email
    if request.method == 'POST':
        invoice_lines = [
            f'Invoice for {request.user.username}',
            f'Email: {request.user.email}',
            ''
            'Items:',
        ]
        for item in items:
            product = item['product']
            quantity = item['quantity']
            line_total = item['line_total']
            invoice_lines.append(
                f'- {product.name} from {product.store.name} '
                f'x {quantity}: £{line_total}'
            )
            product.stock -= quantity
            product.save()
        invoice_lines.extend(
            [
                '',
                f'Total: £{total}',
                '',
                'Thank you for shopping here!'
            ]
        )
        invoice_body = '\n'.join(invoice_lines)
        send_mail(
            subject='Your Invoice',
            message=invoice_body,
            from_email=None,
            recipient_list=[request.user.email or 'shopper@example.com'],
            fail_silently=False
        )
        request.session['basket'] = {}
        request.session.modified = True
        messages.success(request, 'Checkout Complete')
        return redirect('home')
    return render(
        request,
        'shop/checkout.html',
        {
            'items': items,
            'total': total
        }
    )
