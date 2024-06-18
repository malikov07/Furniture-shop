from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=60)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["id"])
        ]

class MaterialType(models.TextChoices):
    Another = ("a", "Another material")
    Wood = ("w","Wood" )
    Iron = ("i","Iron" )
    Marble = ("m", "Marble")
    Granite = ("g", "Granite")
    Soapstone = ("s", "Soapstone")
    Quartz = ("q", "Quartz")
    Cotton = ("c", "Cotton")
    Linen = ("l", "Linen")
    Velvet = ("v", "Velvet")
    Microfiber = ("mic", "Microfiber")
    Polyester = ("p", "Polyester")

class ColorType(models.TextChoices):
    Another = ("a", "Another color")
    Red = ("r", "Red")
    Green = ("g", "Green")
    Blue = ("b", "Blue")
    Yellow = ("y", "Yellow")
    Orange = ("o", "Orange")
    Purple = ("p", "Purple")
    White = ("w", "White")
    Black = ("bk", "Black")
    Gray = ("gr", "Gray")
    Brown = ("br", "Brown")
    Pink = ("pk", "Pink")
    Turquoise = ("t", "Turquoise")

class FurnitureStyleType(models.TextChoices):
    Another = ("a", "Another style")
    Modern = ("mod", "Modern")
    Classic = ("cla", "Classic")
    Traditional = ("tra", "Traditional")
    Contemporary = ("con", "Contemporary")
    Rustic = ("rus", "Rustic")
    Industrial = ("ind", "Industrial")
    Farmhouse = ("far", "Farmhouse")
    Minimalist = ("min", "Minimalist")
    Transitional = ("tran", "Transitional")
    Bohemian = ("boh", "Bohemian")


class Product(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="product_images")
    width = models.PositiveIntegerField(default=50)
    height = models.PositiveIntegerField(default=90)
    deep = models.PositiveIntegerField(default=50)
    color = models.CharField(max_length=10, choices=ColorType.choices, default=ColorType.Another)
    material = models.CharField(max_length=10, choices=MaterialType.choices, default=MaterialType.Another)
    style = models.CharField(max_length=10, choices=FurnitureStyleType.choices, default=FurnitureStyleType.Another)
    company_name = models.CharField(max_length=60, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    warranty_duration = models.PositiveIntegerField( default=12, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True) 

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 
        super().save(*args, **kwargs)
    
    def product_image(self):
        return mark_safe(f"<img src=\"{self.image.url}\" width=\"50px\" height=\"50px\">")

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["id"]),
        ]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(default="img not loaded" ,max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.id}"
    

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)


ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

# class OrderProduct(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)