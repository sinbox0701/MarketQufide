from .models import Product,Comment,Collection
from django import forms

INTEGER_CHOICES= [tuple([x,x]) for x in range(0,6)]

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text', 'like']
        widget = {
            'like' : forms.Select(attrs=INTEGER_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args,**kwargs)
        self.fields['comment_text'].label = "댓글"


