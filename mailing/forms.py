from django import forms
from blog.forms import StyleFormMixin
from mailing.models import Client, MailingMessage, MailingSettings


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('fullname', 'email', 'comment',)


class MailingMessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingMessage
        fields = ('subject', 'body',)


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('start_time', 'stop_time', 'frequency', 'status', 'client', 'message')


class ModeratorMailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('status',)
