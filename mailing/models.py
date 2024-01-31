from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='Фамилия Имя')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Почта')
    comment = models.TextField(verbose_name='Сообщение', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=100, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Письмо')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingSettings(models.Model):
    FREQUENCY = [
        ('daily', 'один раз в день'),
        ('weekly', 'один раз в неделю'),
        ('monthly', 'один раз в месяц')
    ]
    STATUS = [
        ('completed', 'завершена'),
        ('created', 'создана'),
        ('launched', 'запущена')
    ]

    start_time = models.TimeField(default=timezone.now, verbose_name='Время отправления рассылки')
    stop_time = models.TimeField(default=timezone.now, verbose_name='Время окончания рассылки')
    frequency = models.CharField(max_length=50, choices=FREQUENCY, verbose_name='Переодичность')
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='статус')
    client = models.ManyToManyField('Client', verbose_name='клиент')
    message = models.ForeignKey('MailingMessage', on_delete=models.CASCADE, verbose_name='Сообщение')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'Рассылка {self.pk}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class MailingLog(models.Model):
    STATUS = [
        ('successfully', 'успешно'),
        ('fatally', 'фатально')
    ]

    datatime = models.DateTimeField(auto_now_add=True, verbose_name='дата и время попытки')
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='статус попытки')
    serv_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.EmailField(verbose_name='Клиент', **NULLABLE)

    def __str__(self):
        return f'Лог Рассылки: {self.pk}({self.status})'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
