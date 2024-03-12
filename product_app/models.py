from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify

from account_app.models import User
from django.db import models
from django.utils.html import format_html


# Create your models here.

class Ip(models.Model):
    ip = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.ip


class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subs")
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.title:
            self.title = self.title.lower()

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=40, unique=True)
    category = models.ManyToManyField(Category, related_name='categories')
    brand = models.ForeignKey(Brand, related_name="brands", on_delete=models.CASCADE, null=True, blank=True)
    main_image = models.ImageField(upload_to="product-images/")
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    discount_percentage = models.FloatField(null=True, blank=True, default=0,
                                            help_text="If you dont wanna give a discount, put this field free.")
    colors = models.ManyToManyField(Color)
    in_stock = models.BooleanField(default=False)
    buyers = models.ManyToManyField(User, related_name="buyers", editable=False)
    discount = models.BooleanField(default=False, editable=False)
    slug = models.SlugField(unique=True, null=True, blank=True, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    rate = models.IntegerField(null=True, blank=True, default=0)
    likes = models.ManyToManyField(Ip, related_name="liked_posts")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.discount_percentage and self.discount_percentage > 0:
            self.discount = True
        else:
            self.discount = False

        review = Comment.objects.filter(product=self).aggregate(reviews=Avg("rating"))
        avg = 0
        if review['reviews'] is not None:
            avg = float(review['reviews'])
            if avg:
                self.rate = avg

    def get_absolute_url(self):
        return reverse("product_app:product_detail", kwargs={"slug": self.slug})

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title, allow_unicode=True)
        # self.after_discount = self.discount_price()
        super(Product, self).save()

    def __str__(self):
        return self.title

    def show_image(self):
        if self.main_image:
            return format_html(f"<img src='{self.main_image.url}' width='70px' height='70px'>")
        else:
            return format_html(f"<img src='' alt='No Image Available' >")

    def discount_price(self):
        if self.discount_percentage and self.discount_percentage > 0:
            discount_percentage = self.discount_percentage / 100
            first_price = self.price * discount_percentage
            final_price = self.price - first_price
            return final_price
        else:
            return self.price

    def average_review(self):
        review = Comment.objects.filter(product=self).aggregate(reviews=Avg("rating"))
        avg = 0
        if review['reviews'] is not None:
            avg = float(review['reviews'])
        return avg


class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    title = models.CharField(max_length=75)

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product-images")


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    text = models.TextField()
    choices = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    rating = models.IntegerField(null=True, blank=True, choices=choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.text[:20]}"
