from .models import Product,Comment,Collection,Option
from django import forms

INTEGER_CHOICES= [tuple([x,x]) for x in range(0,6)]

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text', 'like', 'comment_image']
        widget = {
            'like' : forms.Select(attrs=INTEGER_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args,**kwargs)
        self.fields['comment_text'].label = "댓글"
        self.fields['comment_image'].required = False
        #file값이 없더라도 view에서 유효성 검사에서 오류를 발생시키지 않도록 해준다.

class OptionForm(forms.ModelForm):

    class Meta:
        model = Option
        fields = ['name', 'add_price', 'stock']

    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.fields[name].label = "옵션"
