from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=255)
    first_name = None
    last_name = None
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, max_length=255)

    REQUIRED_FIELDS = ['username', 'phone', 'name']
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = "users"


# Create your models here.
class Product(models.Model):
    title = models.CharField(verbose_name="Title", max_length=200)
    description = models.TextField(verbose_name="Description")
    current_price = models.PositiveIntegerField(verbose_name="Current Price")
    old_price = models.PositiveIntegerField(verbose_name="Old Price")
    image = models.FileField(upload_to="product_pics/", verbose_name="Product Photo")
    ratings = models.PositiveIntegerField(verbose_name="Ratings")
    num_ratings = models.PositiveIntegerField(verbose_name="Num Ratings")
    size = models.PositiveIntegerField(verbose_name="Size in ml", default=250)
    current_stock = models.IntegerField(verbose_name="Current Stock", default=10)
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date Added")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    then_price = models.PositiveIntegerField(verbose_name="Purchase Price")
    amount = models.PositiveIntegerField(verbose_name="Number Of Items")
    date_purchased = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product) + " By " + str(self.user) + " On " + str(self.date_purchased)

    class Meta:
        db_table = "orders"
        verbose_name_plural = "Orders"
        verbose_name = "Order"

    def save(self, *args, **kwargs):
        product = self.product
        product.current_stock = product.current_stock - self.amount
        product.save()
        super(Order, self).save(*args, **kwargs)
