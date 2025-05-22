import html
from django.conf import settings
from django.shortcuts import redirect, render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from mail.send import send_html_mail

def inquiry_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # HTMLエスケープ（XSS対策）
        escaped_name = html.escape(name)
        escaped_email = html.escape(email)
        escaped_message = html.escape(message)

        # メールバリデーション
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'inquiry/inquiry_form.html', {
                'error': '正しいメールアドレスを入力してください。',
                'name': name,
                'email': email,
                'message': message,
            })

        # ユーザーへの返信内容
        html_content_to_user = f"""
        <html>
          <body>
            <h2>お問い合わせありがとうございます</h2>
            <p>{escaped_name} さん</p>
            <p>以下の内容でお問い合わせを受け付けました。</p>
            <p><strong>メッセージ:</strong> {escaped_message}</p>
            <p>※このメールは自動送信です。</p>
          </body>
        </html>
        """

        # 管理者への通知内容
        html_content_to_admin = f"""
        <html>
          <body>
            <h2>新しいお問い合わせを受信しました</h2>
            <p><strong>名前:</strong> {escaped_name}</p>
            <p><strong>メールアドレス:</strong> {escaped_email}</p>
            <p><strong>内容:</strong> {escaped_message}</p>
          </body>
        </html>
        """

        # ① 管理者へ送信
        send_html_mail(
            subject='【お問い合わせ通知】Webフォームからのメッセージ',
            html_content=html_content_to_admin,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email="takuto.kimura4325@gmail.com",
        )

        # ② ユーザーへ返信
        send_html_mail(
            subject='【自動返信】お問い合わせを受け付けました',
            html_content=html_content_to_user,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_email=email,
        )

        return redirect('inquiry:done')

    return render(request, 'inquiry/inquiry_form.html')


def inquiry_done_view(request):
    return render(request, 'inquiry/inquiry_done.html')
