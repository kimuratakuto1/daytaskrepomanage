from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # 新しいユーザーを作成
            user = form.save()
            # ユーザーをログイン状態にする
            login(request, user)
            # ホームページやユーザーのダッシュボードへリダイレクト
            return redirect('home')  # homeはリダイレクト先のURL名（適宜変更）
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
