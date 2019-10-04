from django import forms
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model, authenticate, login
from .models import SmsSend
from members.models import Marketing, Address

User = get_user_model()


class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=30, label='name')
    phone = forms.CharField(max_length=30, label='phone')

    def signup(self, request, user):
        user.name = self.cleaned_data['name']
        user.phone = self.cleaned_data['phone']
        print("**********************")
        user.save()
        return user

class LogInForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean(self):  # 2개 이상의 필드에 대한 유효성 검사
        cleaned_data = super().clean()  # 부모클래스의 유효성검사는 다 통과했다는 뜻
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        self.user = authenticate(username=email, password=password)
        if not self.user:
            raise forms.ValidationError('Unvalied authentication')
        else:
            setattr(self, 'login', self._login)  # 이때 아래 메소드를 login으로 호출 가능하게 해줌.

    def _login(self, request):
        login(request, self.user)
        
    def clean_verify_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('verify_password')
        if password1 != password2:
            raise forms.ValidationError('Emails must match')
        return password2
      
class SmsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['msg_getter'].required = True
        #self.fields['msg_text'].required = True
    class Meta:
        model = SmsSend
        fields = (
            #'msg_type',
            'msg_getter',
            #'msg_sender',
            #'msg_text'
        )

CHOICES1=[('male','남자'),
         ('female','여자')]

class ProfileForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect())
    birthdate = forms.DateField(widget = forms.SelectDateWidget(years=range(1960, 2019)))
    marketing = forms.ModelMultipleChoiceField(queryset=Marketing.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    class Meta:
        model = User
        fields = ['email', 'first_name', 'phone', 'birthdate', 'sex', 'marketing']


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = ['addr_name', 'phone', 'zip','addr1','addr2']

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args,**kwargs)


class findIDForm(forms.Form):
    username = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=20)


