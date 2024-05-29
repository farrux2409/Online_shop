from django.contrib import admin
from django.contrib.auth.models import User, Group

from app.models import Product, Comment, Category, Order

# Register your models here.

# admin.site.register(Product)
# admin.site.register(Comment)
admin.site.register(Category)


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display = ('costumer', 'phone_number', 'product')

    @admin.register(Product)
    class Product(admin.ModelAdmin):
        list_display = ("name", "image", "price", "discount", "is_expensive")
        list_filter = ("price", "category")

        def is_expensive(self, obj):
            return obj.price > 10_000

        is_expensive.boolean = True


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ("full_name", "product")
    #
    # def name(self, ):
    #     return self.name_set.count()
    #
    # def price(self):
    #     return self.price_set.count()
