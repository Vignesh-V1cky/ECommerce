from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.validators import validate_email
from .storage import OverriteFile

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, date_of_birth, **extra_fields):
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, **extra_fields)
        validate_email(email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        superuser = self.model(username=username, email=email, **extra_fields)
        validate_email(email)
        superuser.set_password(password)
        superuser.date_of_birth = '2000-01-01'
        superuser.is_staff = True
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=255, unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=False, null=False)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now, blank=False, null=False)
    date_joined = models.DateTimeField(default=timezone.now, blank=False, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def str(self):
        return str(self.username)


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        verbose_name_plural = "Categories"

    def str(self):
        return str(self.name)


def get_image_filepath(self, filename):
    return f'./products/{self.name}_{self.created_date_time}.png'


def get_default_image():
    return f'./store/default.png'


class Product(models.Model):
    category = models.ForeignKey("store.Category", on_delete=models.CASCADE, related_name='product_category',
                                 blank=False, null=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    image = models.ImageField(upload_to=get_image_filepath, default=get_default_image, storage=OverriteFile(),
                              blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=True)
    price = models.FloatField(max_length=64, blank=False, null=False)
    is_recommended = models.BooleanField(default=True)
    created_date_time = models.DateTimeField(default=timezone.now, blank=False, null=False)
    is_visible = models.BooleanField(default=True)

    def str(self):
        return str(self.name)


class Order(models.Model):
    PAYMENT_METHODS = [
        ((1, 'Cash/card payment on delivery')),
        ((2, 'Online payment by credit card')),
        ((3, 'Traditional money transfer')),
    ]

    user = models.ForeignKey("store.User", on_delete=models.CASCADE, related_name='order_user', blank=True, null=True)
    payment_method_order = models.IntegerField(choices=PAYMENT_METHODS, default=1, blank=False, null=False)
    country_order = models.CharField(max_length=255, blank=False, null=False)
    city_order = models.CharField(max_length=255, blank=False, null=False)
    street_order = models.CharField(max_length=255, blank=False, null=False)
    house_number_order = models.CharField(max_length=255, blank=False, null=False)
    zip_code_order = models.CharField(max_length=255, blank=False, null=False)
    phone_number_order = models.CharField(max_length=255, blank=False, null=False)
    email_order = models.EmailField(max_length=255, blank=False, null=False)
    date_time_order = models.DateTimeField(default=timezone.now, blank=False, null=False)

    def str(self):
        return str(self.id)


class OrderProduct(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE, related_name='orderproduct_product',
                                blank=False, null=False)
    quantity = models.FloatField(default=1.0, blank=False, null=False)
    order_id = models.ForeignKey("store.Order", on_delete=models.CASCADE, related_name='orderproduct_order_id',
                                 blank=True, null=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def str(self):
        return str(self.id)


class Opinion(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE, related_name='opinion_product',
                                blank=False, null=False)
    user = models.ForeignKey("store.User", on_delete=models.CASCADE, related_name='opinion_user', blank=False,
                             null=False)
    rating = models.CharField(max_length=1, blank=False, null=False, default='5')
    content = models.CharField(max_length=1024, blank=True, null=True)
    created_date_time = models.DateTimeField(default=timezone.now, blank=False, null=False)

    class Meta:
        unique_together = ('product', 'user')

    def str(self):
        return str(self.id)