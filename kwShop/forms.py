
from allauth.account.forms import SignupForm
from django import forms
from members.forms import SmsForm, ConfirmForm

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='이름')

    send_form = SmsForm()
    confirm_form = ConfirmForm()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.save()
        print("*********************************")
        print(self)
        return user