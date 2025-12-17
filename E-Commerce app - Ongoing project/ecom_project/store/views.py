from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import transaction
from .models import Store, Product, BasketItem, OrderItem, Order, Basket, User
from .forms import StoreForm, ProductForm, UserRegisterForm

# Create your views here.


def home(request):
    """Landing page: shows login/register if anonymous, or dashboard link if logged in."""
    return render(request, 'store/home.html', {'user': request.user})


def is_vendor(user):
    return user.groups.filter(name='Vendor').exists()


def is_shopper(user):
    return user.groups.filter(name='Shopper').exists()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Create or get groups
            vendors_group, _ = Group.objects.get_or_create(name='Vendor')
            shoppers_group, _ = Group.objects.get_or_create(name='Shopper')

            # Assign group based on user type
            user_type = form.cleaned_data['role']
            if user_type == 'vendor':
                user.groups.add(vendors_group)
            else:
                user.groups.add(shoppers_group)

            login(request, user)
            return redirect('store_list')
    else:
        form = UserRegisterForm()

    messages.warning(request, form.errors)
    messages.warning(request, form.non_field_errors())
    return render(request, 'store/register.html', {'form': form})


def store_list(request):
    stores = Store.objects.all()
    is_vendor = False
    if request.user.is_authenticated:
        is_vendor = request.user.groups.filter(name='Vendor').exists()

    return render(request, 'store/store_list.html', {
        'stores': stores,
        'is_vendor': is_vendor
    })


def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    products = store.products.filter(store=store)
    return render(request, 'store/store_detail.html',
                  {'store': store, 'products': products})


def custom_login(request):
    """Render plain CSS login form and authenticate user."""
    if request.user.is_authenticated:
        return redirect('store_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('store_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'store/login.html', {'form': form})


@user_passes_test(is_vendor, login_url='login')
def store_create(request):
    if not request.user.groups.filter(name='Vendor').exists():
        messages.error(request, "You must be a vendor to create a store.")
        return redirect('store_list')

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            messages.success(request, f"Store '{store.name}' created " +
                             "successfully!")
            return redirect('store_list')
        else:
            messages.error(request, "There was an error creating your store." +
                           "Please check the form below.")
    else:
        form = StoreForm()

    return render(request, 'store/store_form.html', {'form': form})


@user_passes_test(is_vendor, login_url='login')
def store_edit(request, slug):
    """Allow vendors to edit their store details."""
    store = get_object_or_404(Store, pk=slug)

    if store.owner != request.user:
        messages.error(request, "You are not allowed to edit this store.")
        return redirect('store_list')

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, f"Store '{store.name}' updated successfully!")
            return redirect('store_list')
        else:
            messages.error(request, "There was an error updating your store. Please check the form below.")
    else:
        form = StoreForm(instance=store)

    return render(request, 'store/edit_store.html', {'form': form, 'store': store})


@user_passes_test(is_vendor, login_url='login')
def store_delete(request, slug):
    store = get_object_or_404(Store, slug=slug)
    if store.owner != request.user:
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        store.delete()
        return redirect('store_list')
    return render(request, 'store/store_detail.html', {'store': store, 'confirm_delete': True})


@user_passes_test(is_vendor, login_url='login')
def product_create(request, pk):
    store = get_object_or_404(Store, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            return redirect('store_detail', pk=store.pk)
    else:
        form = ProductForm()

    return render(request, 'store/product_form.html', {'form': form, 'store': store})


@user_passes_test(is_vendor, login_url='login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.store.owner != request.user:
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect(product.store.get_absolute_url())
        else:
            form = ProductForm(instance=product)
        return render(request, 'store/product_form.html', {'form': form, 'product': product})


@user_passes_test(is_vendor, login_url='login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.store.owner != request.user:
        return HttpResponseForbidden('Not allowed')
    if request.method == 'POST':
        store_url = product.store.get_absolute_url()
        product.delete()
        return redirect(store_url)
    return render(request, 'store/product_form.html', {'product': product, 'confirm_delete': True})


@user_passes_test(is_shopper, login_url='login')
def basket_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = BasketItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
        item.save()
        return redirect('basket')


@user_passes_test(is_shopper, login_url='login')
def basket_view(request):
    items = BasketItem.objects.filter(user=request.user).select_related('product')
    total = sum(item.line_total() for item in items)
    return render(request, 'store/basket.html', {'items': items, 'total': total})


@user_passes_test(is_shopper, login_url='login')
def basket_remove(request, item_id):
    item = get_object_or_404(BasketItem, pk=item_id, user=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('basket')
    return render(request, 'store/basket.html', {'confirm_remove': item})


@user_passes_test(is_shopper, login_url='login')
@transaction.atomic
def checkout(request):
    """Convert user's basket into an order and redirect to success page."""
    basket = Basket.objects.filter(user=request.user).first()
    if not basket or basket.items.count() == 0:
        messages.error(request, "Your basket is empty.")
        return redirect('basket')

    # Create Order
    order = Order.objects.create(user=request.user, total=basket.get_total_price())

    # Copy items
    for item in basket.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # Clear basket
    basket.items.all().delete()

    messages.success(request, f"Order #{order.id} placed successfully!")
    return redirect('checkout_success', order_id=order.id)


@user_passes_test(is_shopper, login_url='login')
def checkout_success(request, order_id):
    """Show order confirmation after checkout."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/checkout_success.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(shopper=request.user).order_by('-created_at')
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, shopper=request.user)
    items = order.items.all()
    return render(request, 'store/order_detail.html', {'order': order, 'items': items})


@user_passes_test(is_vendor, login_url='login')
def vendor_orders(request):
    if not request.user.is_vendor(User):
        return HttpResponseForbidden('Only vendors can view this page')
    sold_products = (
        OrderItem.objects.filter(product__store__owner=request.user)
        .values('product_name')
        .annotate(total_sold=sum('quantity'), total_revenue=sum(('quantity') *
                                                                ('price')))
        .order_by('-total_sold')
        )
    return render(request, 'store/vendor_orders.html', {'sold_products': sold_products})


def logout_user(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def product_detail(request, store_id, product_id):
    product = get_object_or_404(Product, id=product_id, store_id=store_id)

    owner = product.store.owner

    # get all stores from this vendor
    vendor_stores = Store.objects.filter(owner=owner)

    # get all products from all of the vendors stores, excluding the
    # current product
    other_products = Product.objects.filter(
        store__owner=owner.stores).exclude(id=product.id)

    context = {
        'product': product,
        'owner': owner,
        'other_products': other_products,
        'vendor_stores': vendor_stores
    }

    return render(request, 'store/product_detail.html', context)
