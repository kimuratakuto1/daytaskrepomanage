from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # 新しいユーザーを作成
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # ユーザーをログイン状態にする
            login(request, user)
            # ホームページやユーザーのダッシュボードへリダイレクト
            return redirect('login')  # homeはリダイレクト先のURL名（適宜変更）
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(requets):
    logout(requets)
    return redirect('login')