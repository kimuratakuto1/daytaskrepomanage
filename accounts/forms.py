from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # パスワード確認などのバリデーションを追加することも可能
    def clean_password(self):
        password = self.cleaned_data.get('password')
        # パスワードの検証（条件追加も可能）
        if len(password) < 8:
            raise forms.ValidationError("パスワードは8文字以上にしてください")
        return password
