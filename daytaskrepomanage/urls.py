from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ↓↓↓ 追加部分（ここから）
import os
import django
from django.core.management import call_command
from django.db import OperationalError
from django.contrib.auth.models import User

django.setup()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('taskmanager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
