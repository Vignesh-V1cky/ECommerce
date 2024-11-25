from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegisterForm, ProfileForm, OrderForm
from .models import Order, Product, Category, OrderProduct, Opinion
from django.core.paginator import Paginator
from django.db.models import Sum, F, Count, Avg
from django.core.mail import EmailMessage

def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'store/login.html', {'form': LoginForm})


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password1'])
            user.save()
            return redirect('login')
        else:
            return render(request, 'store/register.html', {'form': form})
    return render(request, 'store/register.html', {'form': RegisterForm})


def profile_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
            return redirect('home')

        initial_data = {
            'username': request.user.username,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
            'date_of_birth': request.user.date_of_birth,
            'country': request.user.country,
            'city': request.user.city,
            'street': request.user.street,
            'house_number': request.user.house_number,
            'zip_code': request.user.zip_code
        }

        user_orders = Order.objects.filter(user=request.user).order_by('-id')
        paginator = Paginator(user_orders, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        context = {
            'form': ProfileForm(initial=initial_data),
            'page': page
        }
        return render(request, 'store/profile.html', context=context)
    else:
        return redirect('login')


def logout_user(request):
    logout(request)
    return redirect('home')


def home(request):
    products = Product.objects.filter(is_visible=True, is_recommended=True).order_by('-id')
    context = {'products': products}
    return render(request, 'store/home.html', context=context)


def product(request, pk):
    product = Product.objects.get(pk=pk)
    opinions = Opinion.objects.filter(product=pk).order_by('-created_date_time')
    opinions_query = Opinion.objects.filter(product=pk).aggregate(Sum('rating'), Count('id'), Avg('rating'))
    opinions_rating = opinions_query['rating__sum']
    opinions_count = opinions_query['id__count']
    opinions_average_rating = opinions_query[
        'rating__avg'] if opinions_count is not None and opinions_rating is not None else 0
    user_opinion = None

    if request.user.is_authenticated:
        try:
            user_opinion = Opinion.objects.get(user=request.user, product=pk)
        except Opinion.DoesNotExist:
            pass

    context = {
        'product': product,
        'opinions': opinions,
        'opinions_count': opinions_count,
        'opinions_rating': opinions_rating,
        'opinions_average_rating': opinions_average_rating,
        'user_opinion': user_opinion}

    return render(request, 'store/product.html', context=context)


def category_products(request, pk):
    products = Product.objects.filter(is_visible=True, category=pk).order_by('id')
    category = Category.objects.get(pk=pk)
    paginator = Paginator(products, 16)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'category': category}
    return render(request, 'store/category_products.html', context=context)


def searched_products(request):
    products = Product.objects.filter(is_visible=True, name__contains=request.POST['searched']).order_by('id')
    return render(request, 'store/searched_products.html', context={'products': products})

def cart(request):
    initial_data = {}
    pk_cookie, products, cart_total = None, None, None
    cookie = request.COOKIES.get('cart') or None

    if request.user.is_authenticated:
        initial_data = {
            'country_order': request.user.country,
            'city_order': request.user.city,
            'street_order': request.user.street,
            'house_number_order': request.user.house_number,
            'zip_code_order': request.user.zip_code,
            'email_order': request.user.email,
            'phone_number_order': request.user.phone_number,
        }

    if cookie:
        # Split the cookie by underscores
        pk_cookie = []

        for pk_order_product in cookie.split('_'):
            # Check if the current part is a valid integer
            try:
                # Convert to integer, will raise ValueError if invalid
                pk_cookie.append(int(pk_order_product))
            except ValueError:
                # Skip invalid values or handle them as needed
                print(f"Skipping invalid cookie part: {pk_order_product}")
                continue

        if pk_cookie:  # Only proceed if there are valid product IDs
            # Fetch the products and calculate the cart total
            products = OrderProduct.objects.filter(pk__in=pk_cookie)
            cart_total = OrderProduct.objects.filter(pk__in=pk_cookie).annotate(
                orderproduct_total=F('product__price') * F('quantity')
            ).aggregate(total=Sum('orderproduct_total'))['total']
        else:
            # Handle the case where no valid products are in the cookie
            products = []
            cart_total = 0.0

    else:
        # If there's no cookie, handle the case appropriately
        products = []
        cart_total = 0.0

    # Pass the products and total to the context for rendering
    context = {
        'products': products,
        'cart_total': cart_total,
        'form': OrderForm(initial=initial_data)
    }

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            order.user = request.user if request.user.is_authenticated else None
            order.payment_method_order = request.POST['payment_method_order']
            OrderProduct.objects.filter(pk__in=pk_cookie).update(order_id=order.pk)
            order.save()
            response = redirect('complete_order')
            response.delete_cookie('cart')
            email = EmailMessage('Your order is ready', f'Your order has been assigned a number #{order.pk}',
                                 to=[order.email_order])
            email.send()
            return response
    return render(request, 'store/cart.html', context=context)


def cart_action(request, pk):
    response = redirect('cart')  # Redirect to the cart page after action
    action = request.GET.get('action')
    cookie = request.COOKIES.get('cart') or None

    if action == 'add':
        product = Product.objects.get(pk=pk)
        if cookie:
            # Process the cookie value and handle invalid data like '{}'
            pk_cookie = []
            for pk_order_product in cookie.split('_'):
                try:
                    pk_cookie.append(int(pk_order_product))
                except ValueError:
                    # Log the invalid part (e.g., '{}') for debugging
                    print(f"Skipping invalid cookie part: {pk_order_product}")
                    continue

            # Fetch the order products
            order_products = OrderProduct.objects.filter(pk__in=pk_cookie)
            found = any(item.product.pk == pk for item in order_products)

            if found:
                # If the product is already in the cart, increase the quantity
                order_product = OrderProduct.objects.get(pk__in=pk_cookie, product=product)
                order_product.quantity += 1
                order_product.save()
            else:
                # If product not found, create a new order product
                new_product = OrderProduct.objects.create(product=product)
                response.set_cookie(key='cart', value=f'{cookie}_{new_product.pk}')
        else:
            # If no cookie exists, create the first product entry in the cart
            new_product = OrderProduct.objects.create(product=product)
            response.set_cookie(key='cart', value=f'{new_product.pk}')

    elif action == 'remove':
        if cookie:
            # Process the cookie value and handle invalid data like '{}'
            pk_cookie = []
            for pk_order_product in cookie.split('_'):
                try:
                    pk_cookie.append(int(pk_order_product))
                except ValueError:
                    # Log the invalid part (e.g., '{}') for debugging
                    print(f"Skipping invalid cookie part: {pk_order_product}")
                    continue

            # Remove the specified product from the cart
            pk_cookie.remove(pk)
            if len(pk_cookie) > 0:
                response.set_cookie(key='cart', value="_".join(map(str, pk_cookie)))
            else:
                response.delete_cookie('cart')

            # Remove the OrderProduct instance from the database
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

    return response


def cart_quantity(request, pk):
    response = redirect('cart')
    order_product = OrderProduct.objects.get(pk=pk)
    action = request.GET.get('action')
    if action == 'add':
        order_product.quantity += 1

    elif action == 'remove':
        order_product.quantity -= 1

    if order_product.quantity == 0:
        cookie = request.COOKIES.get('cart') or None
        pk_cookie = [int(pk_order_product) for pk_order_product in cookie.split('_')]
        pk_cookie.remove(pk)

        if len(pk_cookie) > 0:
            response.set_cookie(key='cart', value="_".join(map(str, pk_cookie)))
        else:
            response.delete_cookie('cart')
        order_product.delete()
    else:
        order_product.save()

    return response


def complete_order(request):
    return render(request, 'store/complete_order.html')


def opinion_action(request, pk):
    if request.user.is_authenticated:
        action = request.GET.get('action')
        if action == 'add':
            product = Product.objects.get(pk=pk)
            Opinion.objects.create(user=request.user, product=product, rating=request.POST['rating'],
                                   content=request.POST['content'])
        elif action == 'remove':
            opinion = Opinion.objects.get(user=request.user, product=pk)
            opinion.delete()
        return redirect('product', pk=pk)


def user_order(request, pk):
    order = Order.objects.get(pk=pk)
    if order.user == request.user:
        order_products = OrderProduct.objects.filter(order_id=order)
        cart_total = OrderProduct.objects.filter(order_id=order).annotate(
            orderproduct_total=F('product__price') * F('quantity')).aggregate(total=Sum('orderproduct_total'))['total']
        context = {
            'order': order,
            'order_products': order_products,
            'cart_total': cart_total
        }
        return render(request, 'store/user_order.html', context=context)
    else:
        return redirect('home')