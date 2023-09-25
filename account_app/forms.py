from django import forms
from django.core import validators
from django.core.validators import ValidationError


def start_with_0(value):
    if value[0] != "0":
        raise forms.ValidationError("phone should start with 0")


class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput, validators=[start_with_0])
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) != 11:
            raise ValidationError("Your phonenumber is short", code="invalid_phone",
                                  params={'value': f'{phone}'})
        return phone


class OtpLoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Your PhoneNumber'}),
                            validators=[start_with_0])

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) > 11:
            #           We can use this code except of validators.MaxLenghtValidator
            raise ValidationError("entered phone number is not valid!", code="invalid_phone",
                                  params={'value': f'{phone}'})
        return phone


class CheckOtpForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Enter your code here'}),
                           validators=[validators.MaxLengthValidator(4)])
