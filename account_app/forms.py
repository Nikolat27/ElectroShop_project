from django import forms
from django.contrib.auth import login, logout, authenticate
from .models import User
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username: ", max_length=30, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))
    email = forms.EmailField(label="Email: ", max_length=40, required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))
    pass1 = forms.CharField(label="password: ", max_length=80, required=True,
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))
    pass2 = forms.CharField(label="ReEnter your password: ", max_length=80, required=True,
                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width: auto;'}))

    # def clean_password2(self):
    #     cd = self.cleaned_data
    #     password1 = cd.get("pass1")
    #     password2 = cd.get("pass2")
    #
    #     if password1 and password2 and password1 != password2:
    #         raise ValidationError(password2, "passwords does not match")

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

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')
        else:
            raise ValidationError("Your username or password is incorrect")
