from datetime import datetime
from smtplib import SMTPException
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from mailing.models import MailingLog, MailingMessage


def send_mailing(mailing):
    """Отправление рассылки по почте и создание логов рассылки"""
    now = datetime.now().time()
    if mailing.start_time <= now <= mailing.stop_time:
        for client in mailing.client.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client],
                    fail_silently=False
                )
                log = MailingLog.objects.create(
                    datatime=mailing.start_time,
                    status='successfully',
                    mailing=mailing,
                    client=client.email,
                )
                log.save()

            except SMTPException as error:
                log = MailingLog.objects.create(
                    datatime=mailing.start_time,
                    status='fatally',
                    mailing=mailing,
                    serv_response=error,
                    client=client.email,
                )
                log.save()


def get_message():
    if settings.CACHE_ENABLED:
        message = cache.get('message')
        if message is None:
            message = MailingMessage.objects.all()
            cache.set('message', message)
    else:
        message = MailingMessage.objects.all()

    return message
