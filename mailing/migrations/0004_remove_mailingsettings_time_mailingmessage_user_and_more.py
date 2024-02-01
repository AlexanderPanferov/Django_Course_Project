# Generated by Django 4.2.5 on 2024-01-31 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mailing', '0003_mailingsettings_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailingsettings',
            name='time',
        ),
        migrations.AddField(
            model_name='mailingmessage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Время отправления рассылки'),
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='stop_time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Время окончания рассылки'),
        ),
    ]