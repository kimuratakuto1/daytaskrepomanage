# mail/views.py

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
import json

@csrf_exempt  # 仮でCSRFを無効化（開発中用）
def send_mail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            subject = f'お問い合わせ: {name}さんより'
            body = f'名前: {name}\nメール: {email}\n\nメッセージ:\n{message}'

            send_mail(
                subject,
                body,
                email,  # 送信元（ユーザーのメール）
                ['あなたのメールアドレス@example.com'],  # 宛先
                fail_silently=False,
            )

            return JsonResponse({'message': '送信成功！'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'POSTで送ってください'}, status=400)
