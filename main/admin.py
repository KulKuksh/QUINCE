from django.contrib import admin
from .models import User, Category, Dish, CartItem, Order, OrderItem, Review

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)