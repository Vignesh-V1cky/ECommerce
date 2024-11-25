from django.contrib import admin
from .models import User
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Category, Product, Order, OrderProduct, Opinion

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('id', 'username', 'email', 'date_of_birth', 'phone_number',  'country',
                    'city', 'street', 'house_number', 'zip_code', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'date_of_birth', 'phone_number', 'country',
                    'city', 'street', 'house_number', 'zip_code', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
                }
        ),)
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'date_of_birth', 'password1', 'password2',  'is_staff', 'is_active', 'is_superuser',)
            }
        ),)

admin.site.register(User, UserAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'image', 'description',
                    'price', 'is_recommended', 'created_date_time', 'is_visible')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_method_order', 'country_order',
                    'city_order', 'street_order', 'house_number_order', 'zip_code_order', 'phone_number_order', 'email_order', 'date_time_order')


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'order_id')


class OpinionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating',
                    'content', 'created_date_time')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Opinion, OpinionAdmin)