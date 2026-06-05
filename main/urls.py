from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from main.sitemaps import DishSitemap, CategorySitemap

sitemaps = {
    'dishes': DishSitemap,
    'categories': CategorySitemap,
}


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('dish/<slug:slug>/', views.dish_detail, name='dish_detail'),
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
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]