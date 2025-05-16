from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm
from django.conf import settings
from decouple import config

#サインアップ可否の環境変数、許可時はTrueに
ALLOW_SIGNUP = config('ALLOW_SIGNUP', default=False, cast=bool)


from django.conf import settings

def signup(request):
    if not settings.ALLOW_SIGNUP:
        return redirect('login')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(requets):
    logout(requets)
    return redirect('login')