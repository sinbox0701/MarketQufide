from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, authenticate, login

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
