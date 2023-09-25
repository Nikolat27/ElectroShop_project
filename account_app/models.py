from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from datetime import timedelta, datetime


class MyUserManager(BaseUserManager):
    def create_user(self, phone=None, password=None, username=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an Phone Number")

        user = self.model(
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password, email=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    prof_pic = models.ImageField(upload_to="img/prof_pics", null=True, blank=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class OTP(models.Model):
    token = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=11, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    code = models.SmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    expiration_code = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.phone
