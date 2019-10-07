
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label='이름')
    phone = forms.CharField(max_length=30, label='핸드폰번호')
    birthdate = forms.DateField(label='생년월일')
    sex = forms.CharField(label='성별')

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.phone = self.cleaned_data['phone']
        user.name = self.cleaned_data['name']
        user.birthdate = self.cleaned_data['birthdate']
        user.sex = self.cleaned_data['sex']
        user.save()
        return user
    '''
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(max_length=30, label='name')
        self.fields['phone'] = forms.CharField(max_length=30, label='phone')

        # You don't want the `remember` field?
        #if 'remember' in self.fields.keys():
         #   del self.fields['remember']
    
    def signup(self, request, user):
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        print("**********************")
        user.save()
        return user
    '''
