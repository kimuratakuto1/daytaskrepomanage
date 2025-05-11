from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='パスワード')
    password2 = forms.CharField(widget=forms.PasswordInput, label='パスワード（確認）')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # パスワード確認のバリデーション
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("パスワードが一致しません")
        
        if len(password) < 8:
            raise forms.ValidationError("パスワードは8文字以上にしてください")
        
        return password2
