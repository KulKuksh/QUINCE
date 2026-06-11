from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),
    path('add-review/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('reviews/', views.reviews, name='reviews'),
    path('profile/', views.profile, name='profile'),
    path('contacts/', views.contacts, name='contacts'),
]