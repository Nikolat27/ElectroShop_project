from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review", "class": "input", "id": 'body'})
                           , required=False)
    parent_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Parent Id", 'type': "hidden",
                                                              "class": "input", 'id': 'parent_id'}))

    class Meta:
        model = Comment
        fields = ['body', 'parent_id']

