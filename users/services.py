from django.conf import settings
from django.core.mail import send_mail


def send_new_password(email, new_password):
    send_mail(
        subject='Смена пароля',
        message=f'Новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


def send_verification_link(email, verification_code):
    send_mail(
        subject='Подтверждение адреса электронной почты',
        message=f'ссылка для верификации: http://127.0.0.1:8000/users/verify?code={verification_code}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )
