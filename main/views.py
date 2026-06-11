from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Dish, CartItem, Order, OrderItem, Review
from .forms import UserRegisterForm
from django.core.paginator import Paginator



def home(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(is_available=True)[:6]
    return render(request, 'main/home.html', {'categories': categories, 'dishes': dishes})

def menu(request):
    categories = Category.objects.all()
    dishes_list = Dish.objects.filter(is_available=True).select_related('category').order_by('id')
    paginator = Paginator(dishes_list, 12)
    page_number = request.GET.get('page')
    dishes = paginator.get_page(page_number)
    return render(request, 'main/menu.html', {'categories': categories, 'dishes': dishes})



@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total() for item in cart_items)
    return render(request, 'main/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, dish=dish)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{dish.name} добавлен в корзину')
    return redirect('menu')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items:
        return redirect('menu')
    total = sum(item.get_total() for item in cart_items)
    
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        delivery_type = request.POST.get('delivery_type')
        comment = request.POST.get('comment', '')
        payment_method = request.POST.get('payment_method')
        if delivery_type == 'pickup':
            delivery_cost = 0
        elif delivery_type == 'delivery_inside':
            delivery_cost = 0 if total >= 1200 else 200
        else:
            delivery_cost = 200
        total_amount = total + delivery_cost
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            delivery_cost=delivery_cost,
            address=address,
            phone=phone,
            comment=comment,
            payment_method=payment_method, 
        )
        for item in cart_items:
            OrderItem.objects.create(order=order, dish=item.dish, quantity=item.quantity, price=item.dish.price)
        cart_items.delete()
        messages.success(request, f'Заказ №{order.id} оформлен! Сумма: {total_amount} ₽')
        return redirect('order_history')
    return render(request, 'main/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/order_history.html', {'orders': orders})

@login_required
def add_review(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        rating = int(request.POST.get('rating'))
        Review.objects.create(user=request.user, text=text, rating=rating, status='pending')
        messages.success(request, 'Спасибо за отзыв! Он будет опубликован после модерации.')
        return redirect('home')
    return render(request, 'main/add_review.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def clear_cart(request):
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, 'Корзина очищена')
    return redirect('cart')


def reviews(request):
    reviews_list = Review.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'main/reviews.html', {'reviews': reviews_list})

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    reviews = Review.objects.filter(user=user).order_by('-created_at')
    return render(request, 'main/profile.html', {'orders': orders, 'reviews': reviews})

def contacts(request):
    return render(request, 'main/contacts.html')