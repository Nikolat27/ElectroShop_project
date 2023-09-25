
from django.db import models
from django.db.models import Model, Avg
from django.urls import reverse
from django.utils.text import slugify
from django.utils.html import format_html
from django.utils import timezone

from account_app.models import User


# Create your models here.
class Category(Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, related_name="subs", null=True, blank=True)
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Size(Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Color(Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    discount = models.SmallIntegerField(null=True, blank=True, default=0)
    image = models.ImageField(upload_to="images/product_pics")
    image2 = models.ImageField(upload_to="images/product_pics", null=True, blank=True)
    image3 = models.ImageField(upload_to="images/product_pics", null=True, blank=True)
    image4 = models.ImageField(upload_to="images/product_pics", null=True, blank=True)
    size = models.ManyToManyField(Size, related_name="sizes")
    color = models.ManyToManyField(Color, related_name="colors")
    quantity = models.IntegerField()
    category = models.ManyToManyField(Category, related_name="category")
    slug = models.SlugField(null=True, blank=True, allow_unicode=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Product, self).save()

    def discount_price(self):
        if self.discount != 0:
            discount_price = self.price * self.discount // 100  #1st. We should calculate the percentage of the discount
            total_price = self.price - discount_price           #2st. We should create another variable and minus the price
                                                                #to our discound price!
            return total_price                                  #And now we will return the price with applied discount

    def averagereview(self):
        review = Review.objects.filter(product=self).aggregate(reviews=Avg('rating'))
        avg = 0
        if review["reviews"] is not None:
            avg = float(review["reviews"])
        return avg

    def get_absolute_url(self):
        return reverse("products_app:detail", kwargs={"slug": self.slug})

    def show_image(self):
        if self.image:
            return format_html(f"<img src='{self.image.url}' width='70px' height='70px'>")
        else:
            return format_html(f"<img src="" width='70px' height='70px' alt='No Image!'>")


class Information(Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.text:30}"


class Like(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} - {self.product.title}"


class Comment(Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.product} - {self.body:30}"


class Review(Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    RATING = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))
    rating = models.IntegerField(choices=RATING, null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.product} - {self.author.username}"


class Contact(Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    subject = models.CharField(max_length=50, null=True, blank=True)
    massage = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.subject:15}"

