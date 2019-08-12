from django import forms
from .models import *

class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ('content', 'image','password', )