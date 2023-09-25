from django import forms


class CouponApplyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={"class": "input", "placeholder": "apply your coupon here"})
                           , required=False)
