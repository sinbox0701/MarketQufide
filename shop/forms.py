from .models import Product,Comment
from django import forms

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['comment_text'].label = "댓글"
