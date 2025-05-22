# inquiry/urls.py
from django.urls import path
from .views import inquiry_view, inquiry_done_view

app_name = "inquiry"

urlpatterns = [
    path('', inquiry_view, name='form'),
    path('done/', inquiry_done_view, name='done'),
]
