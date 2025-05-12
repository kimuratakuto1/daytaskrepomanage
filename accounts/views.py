from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm
from django.conf import settings

def signup(request):
    return redirect('login')

def logout_view(requets):
    logout(requets)
    return redirect('login')