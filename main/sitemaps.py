from django.contrib.sitemaps import Sitemap
from .models import Category, Dish

class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.created_at if hasattr(obj, 'created_at') else None

class DishSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Dish.objects.filter(is_available=True)   # только доступные

    def lastmod(self, obj):
        return obj.created_at if hasattr(obj, 'created_at') else None