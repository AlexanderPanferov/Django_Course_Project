from django.contrib import admin

from mailing.models import Client, MailingMessage, MailingSettings, MailingLog

admin.site.register(Client)
admin.site.register(MailingMessage)
admin.site.register(MailingSettings)
admin.site.register(MailingLog)
