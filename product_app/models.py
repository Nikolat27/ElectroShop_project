from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.urls import reverse
from django.utils.text import slugify
from django.contrib import messages
from account_app.models import User
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext as _


# Create your models here.

class Ip(models.Model):
    ip = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.ip


class Category(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subs")
    title = models.CharField(max_length=50, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.parent is None:
            if Category.objects.filter(parent__title=self.title).count() >= 2:
                self.date_error_message(self, field_name="title", unique_for="title")
        else:
            if Category.objects.filter(parent__title=self.title).count() >= 2:
                return

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
    discount_percentage = models.FloatField(null=True, blank=True, default=0,
                                            help_text="If you dont wanna give a discount, put this field free.")
    buyers = models.ManyToManyField(User, related_name="buyers", editable=False)
    discount = models.BooleanField(default=False, editable=False)
    slug = models.SlugField(unique=True, null=True, blank=True, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.discount_percentage and self.discount_percentage > 0:
            self.discount = True
        elif not self.discount_percentage or self.discount_percentage <= 0:
            self.discount = False

    def get_absolute_url(self):
        return reverse("product_app:product_detail", kwargs={"slug": self.slug})

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title, allow_unicode=True)
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

    @property
    def is_available(self):
        for product_color in self.product_colors.all():
            if not product_color.in_stock or product_color.quantity <= 0:
                return False
        return True


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_colors")
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    in_stock = models.BooleanField(default=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.color:
    #         return
    #     else:
    #         if self.quantity and self.quantity == 0:
    #             self.in_stock = False
    #             self.save()
    #         elif self.quantity and self.quantity >= 1:
    #             self.in_stock = True
    #             self.save()

    def save(self, *args, **kwargs):
        if not self.color:
            return  # Do not save if color is null

        if self.quantity == 0:
            self.in_stock = False
        elif self.quantity >= 1:
            self.in_stock = True

        super(ProductColor, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - {self.color.title} - {self.quantity}"


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


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_likes")

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
