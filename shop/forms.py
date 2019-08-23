from .models import Product,Comment,Collection
from django import forms

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text', 'like']


    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args,**kwargs)
        self.fields['comment_text'].label = "댓글"


