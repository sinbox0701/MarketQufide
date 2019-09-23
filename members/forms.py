from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login
from members.models import Marketing

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)

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

CHOICES1=[('male','남자'),
         ('female','여자')]

class ProfileForm(forms.ModelForm):
    sex = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect())
    birthdate = forms.DateField(widget = forms.SelectDateWidget(years=range(1960, 2019)))
    marketing = forms.ModelMultipleChoiceField(queryset=Marketing.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    class Meta:
        model = User
        fields = ['email', 'username', 'phone', 'birthdate', 'sex', 'marketing']
