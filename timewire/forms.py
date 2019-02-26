from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.forms.fields import EmailField
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Work

class LoginForm(forms.Form):
    # username = UsernameField(
    #     label = 'ユーザー名',
    #     max_length=255,
    # )
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'placeholder': 'メールアドレス'}),

    )

    password = forms.CharField(
        label='パスワード',
        strip=False,
        widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'パスワード'}),
    )

# clean_メソッド名　バリデーション
#     def clean_username(self):
#         username = self.cleaned_data['username']
#         if len(username) < 3:
#             raise forms.ValidationError(
#                 '%(min_length)s 文字以上で入力してください', params={'min_length': 3})
#             return username

# clean バリデーション

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError("正しいメールアドレスを入力してください")
        if not user.check_password(password):
            raise forms.ValidationError("正しいパスワードを入力してください")


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'ユーザー名'}),
            # 'email': forms.EmailInput(attrs={'placeholder': 'メールアドレス'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'パスワード'}),
        }
    # email = EmailField(
    #     label='メールアドレス',
    #     widget=forms.EmailInput(attrs={'placeholder': 'メールアドレス'}),
    # )
    #
    # username = UsernameField(
    #     label='ユーザー名',
    #     max_length=255,
    #     widget=forms.TextInput(attrs={'placeholder': 'ユーザー名', 'autofocus': True}),
    # )
    # password = forms.CharField(
    #     label='パスワード',
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}),
    # )
    password2 = forms.CharField(
        label='確認用パスワード',
        required=True,
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': '確認用パスワード'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['email'].widget.attrs = {'placeholder': 'メールアドレス'}

    def clean_username(self):
        value = self.cleaned_data['username']
        if value == '':
            raise forms.ValidationError(
                'ユーザー名を入力してください'
            )
        return value

    def clean_email(self):
        value = self.cleaned_data['email']
        return value

    def clean_password(self):
        value = self.cleaned_data['password']
        return value

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("確認用パスワードと一致していません")
        super().clean()


class PostForm(forms.Form):
    class Meta:
        model = Work
        fields = ('name', 'price', 'content')

    name = forms.CharField(
        label='店舗名',
        widget=forms.TextInput(attrs={'placeholder': '店舗名'}),
    )
    price = forms.IntegerField(
        label='時給',
        widget=forms.TextInput(attrs={'placeholder': '時給'}),
    )
    content = forms.CharField(
        label='案件詳細',
        widget=forms.Textarea(attrs={'placeholder': '案件詳細'}),
    )

    def clean_name(self):
        value = self.cleaned_data['name']
        return value

    def clean_price(self):
        value = self.cleaned_data['price']
        return value

    def clean_content(self):
        value = self.cleaned_data['content']
        return value

