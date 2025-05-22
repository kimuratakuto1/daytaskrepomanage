# inquiry/forms.py
from django import forms

class InquiryForm(forms.Form):
    name = forms.CharField(label="お名前", max_length=100)
    email = forms.EmailField(label="メールアドレス")
    message = forms.CharField(label="お問い合わせ内容", widget=forms.Textarea)
