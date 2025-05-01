import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daytaskrepomanage.settings')
django.setup()

# 👇 ここでマイグレーション
from django.core.management import call_command
try:
    call_command('migrate')
    call_command('collectstatic', '--noinput')
except Exception as e:
    print(f"Error during startup migration or collectstatic: {e}")

application = get_wsgi_application()
