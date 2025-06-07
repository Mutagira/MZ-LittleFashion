from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Customer, ShippingAddress, Cart, Order, ContactMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomerProfileForm, ShippingAddressForm

def home(request):
    featured_products = Product.objects.all()[:4]
    return render(request, 'index.html', {'products': featured_products})

def products(request):
    products_list = Product.objects.all()
    return render(request, 'products.html', {'products': products_list})

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    related_products = Product.objects.filter(category=product.category).exclude(pk=id)[:4]
    return render(request, 'product-detail.html', {'product': product, 'related_products': related_products})


def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username= username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
           messages.error(request, "Invalid username or password")
           return redirect('login')

    else:
      return render(request, 'login.html')

def log_out(request):
   logout(request)
   messages.success(request, "You have been logged out!")
   return redirect('home')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('sign_up')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('sign_up')


        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)  # Log the user in after signup
        messages.success(request, "Signup successful!")
        return redirect('home')

    return render(request, 'sign-up.html')   


def contact(request):
      if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message
        )

        messages.success(request, "Thank you for your message! We'll get back to you soon.")
        return redirect("contact")
      return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def faq(request):
    return render(request, 'faq.html')     


@login_required
def profile_view(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile') 
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomerProfileForm(instance=customer)

    context = {'form': form, 'customer': customer}
    return render(request, 'profile.html', context)


@login_required
def address_view(request):
    try:
        address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        address = None
    return render(request, 'address.html', {'address': address})




@login_required
def add_address(request):
    try:
        address = request.user.shippingaddress
        return redirect('update-address')  
    except ShippingAddress.DoesNotExist:
        pass

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.profile = request.user.customer    
            shipping_address.save()
            return redirect('address')  
    else:
        form = ShippingAddressForm()

    context = {'form': form}
    return render(request, 'add_address.html', context)


@login_required
def update_address(request):
    address = get_object_or_404(ShippingAddress, user=request.user)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ShippingAddressForm(instance=address)
    
    context = {'form': form}
    return render(request, 'update_address.html', context)




@login_required
def add_to_cart(request):
    product_id = request.GET.get('product_id')
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')



@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items,'subtotal': subtotal,})


@login_required
def delete_cart_item(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')


@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete() 
    return redirect('view_cart')


def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    shipping_address = ShippingAddress.objects.filter(user=user).first()

    if not cart_items.exists():
        return redirect('cart')

    total_cart_price = sum(item.total_price for item in cart_items)
    shipping_price = 170
    total_price = total_cart_price + shipping_price

    context = {
        'cart_items': cart_items,
        'shipping_address': shipping_address,
        'total_cart_price': total_cart_price,
        'shipping_price': shipping_price,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)



@login_required
def place_order(request):
    if request.method == 'POST':
        address_id = request.POST.get('address')
        payment_method = request.POST.get('payment')
        address = get_object_or_404(ShippingAddress, id=address_id)
        cart_items = Cart.objects.filter(user=request.user)
        customer = Customer.objects.get(user=request.user)

        for item in cart_items:
            Order.objects.create(
                user=request.user,
                customer=customer,
                product=item.product,
                quantity=item.quantity,
                shipping_address=address,
                payment_method=payment_method,
                is_paid=(payment_method != 'COD')  
            )

        cart_items.delete()
        return redirect('view_cart')

    return redirect('checkout')

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user_orders.html', {'orders': orders})