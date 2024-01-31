from mailing.models import MailingSettings
from mailing.services import send_mailing


def daily_tasks():
    mailings = MailingSettings.objects.filter(frequency="daily", status='launched')
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def weekly_tasks():
    mailings = MailingSettings.objects.filter(frequency="weekly", status='launched')
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)


def monthly_tasks():
    mailings = MailingSettings.objects.filter(frequency="monthly", status='launched')
    if mailings.exists():
        for mailing in mailings:
            send_mailing(mailing)
