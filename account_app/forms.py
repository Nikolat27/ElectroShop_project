from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import login, authenticate

from cart_app.models import Cart
from .models import User
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username: ", max_length=30, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))
    email = forms.EmailField(label="Email: ", max_length=40, required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))
    pass1 = forms.CharField(label="password: ", max_length=80, required=True,
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))
    pass2 = forms.CharField(label="ReEnter your password: ", max_length=80, required=True,
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))

    def clean(self):
        cleaned_data = super().clean()
        pass1 = cleaned_data['pass1']
        pass2 = cleaned_data['pass2']
        email = cleaned_data['email']
        username = cleaned_data['username']

        if pass1 and pass2 and pass1 == pass2:
            if email:
                email_check = User.objects.filter(email=email).exists()
                if email_check is True:
                    raise forms.ValidationError('Email is already registered')
                else:
                    if username:
                        username_check = User.objects.filter(username=username).exists()
                        if username_check is True:
                            raise forms.ValidationError('Username is already registered')
                        else:
                            User.objects.create_user(username=username, email=email, password=pass1)
                    else:
                        raise ValidationError("Please Enter an Username")
            else:
                raise ValidationError("Please Enter an Email")
        else:
            raise ValidationError('Passwords dont match')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs={'class': "form-control", 'style': 'width: auto;'}))
    password = forms.CharField(max_length=80,
                               widget=forms.PasswordInput(attrs={'class': "form-control", 'style': 'width: auto;'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        cleaned_data = super().clean()

        username = cleaned_data['username']
        password = cleaned_data['password']

        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')

            session_id = request.session.get("anonymous_user")
            anonymous_cart = Cart.objects.filter(session_id=session_id).first()
            user_cart = Cart.objects.filter(user=user).first()
            if anonymous_cart:
                if user_cart:
                    for item in anonymous_cart.cart_items.all():
                        print(item.product.title)
                        user_cart.cart_items.add(item)
                    anonymous_cart.delete()
                else:
                    anonymous_cart.user = user
                    anonymous_cart.session_id = None
                    anonymous_cart.save()
        else:
            raise ValidationError("Your username or password is incorrect")


class CaptchaTestForm(forms.Form):
    captcha_field = CaptchaField()


class FormWithCaptcha(forms.Form):
    captcha = ReCaptchaField()
