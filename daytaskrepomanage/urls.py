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

try:
    # 自動でマイグレーションを実行
    call_command('migrate', interactive=False)

    # スーパーユーザーがまだ存在しなければ作成
    username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'yourpassword')

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print("スーパーユーザーを作成しました。")
except OperationalError as e:
    print("マイグレーションまたはユーザー作成エラー:", e)
# ↑↑↑ 追加部分（ここまで）

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('taskmanager.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
