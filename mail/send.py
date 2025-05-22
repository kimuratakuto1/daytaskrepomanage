import smtplib
import ssl
import certifi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_html_mail(subject, html_content, from_email, to_email):
    # メールの作成
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    # SSLの設定（certifiでルート証明書を明示）
    context = ssl.create_default_context(cafile=certifi.where())

    # SMTPサーバへ接続（SSL）
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(from_email, os.getenv("EMAIL_HOST_PASSWORD"))
        server.sendmail(from_email, to_email, msg.as_string())
