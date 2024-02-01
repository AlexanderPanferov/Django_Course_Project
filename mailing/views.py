import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from blog.models import Blog
from mailing.forms import ClientForm, MailingMessageForm, MailingSettingsForm, ModeratorMailingSettingsForm
from mailing.models import Client, MailingMessage, MailingSettings, MailingLog
from mailing.services import get_message


class HomepageView(TemplateView):
    """Отображение главной страницы"""
    template_name = 'mailing/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_settings'] = len(MailingSettings.objects.all())
        context_data['mailing_active'] = MailingSettings.objects.filter(status='launched').count()
        context_data['client'] = len(Client.objects.all())
        context_data['blog_list'] = random.sample(list(Blog.objects.all()), 3)

        return context_data


class MailingLogListView(LoginRequiredMixin, ListView):
    """Отображение списка рассылок"""
    model = MailingLog

    def get_queryset(self):
        """Функция для просмотра только своих логов"""
        if self.request.user.groups.filter(name='mailing_mod').exists():
            return MailingLog.objects.all()
        queryset = MailingLog.objects.filter(mailing__user=self.request.user)
        return queryset


class ClientListView(LoginRequiredMixin, ListView):
    """Отображение списка клиентов"""
    model = Client

    def get_queryset(self):
        """Функция для просмотра только своих клиентов"""
        queryset = super().get_queryset().filter()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class ClientCreateView(CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')

    def form_valid(self, form):
        """Функция для присвоения клиента к пользователю"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    """Редактирование клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')


class ClientDetailView(DetailView):
    """Просмотр клиента"""
    model = Client


class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('mailing:list_client')


class MailingMessageListView(LoginRequiredMixin, ListView):
    """Отображение списка сообщений"""
    model = MailingMessage

    def get_queryset(self):
        """Функция, позволяющая просматривать только своих клиентов"""
        queryset = super().get_queryset().filter()
        if self.request.user.groups.filter(name='mailing_mod').exists():
            return queryset
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MailingMessageCreateView(CreateView):
    """Создание сообщения"""
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:list_message')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingMessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    success_url = reverse_lazy('mailing:list_message')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class MailingMessageDetailView(DetailView):
    """Просмотр сообщения"""
    model = MailingMessage


class MailingMessageDeleteView(DeleteView):
    """Удаление сообщения"""
    model = MailingMessage
    success_url = reverse_lazy('mailing:list_message')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class MailingSettingsListView(LoginRequiredMixin, ListView):
    """Отображение списка рассылок"""
    model = MailingSettings

    def get_context_data(self, **kwargs):
        """Кеширование сообщений"""
        context_data = super().get_context_data(**kwargs)
        context_data['message'] = get_message()
        return context_data

    def get_queryset(self):
        queryset = super().get_queryset().filter()
        if self.request.user.groups.filter(name='mailing_mod').exists():
            return queryset
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MailingSettingsCreateView(CreateView):
    """Создание рассылок"""
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:list_settings')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(UpdateView):
    """Редактирование рассылок"""
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:list_settings')

    def get_form_class(self):
        if self.object.user == self.request.user:
            return MailingSettingsForm
        if self.request.user.groups.filter(name='mailing_mod').exists():
            return ModeratorMailingSettingsForm


class MailingSettingsDetailView(DetailView):
    """Просмотр рассылок"""
    model = MailingSettings


class MailingSettingsDeleteView(DeleteView):
    """Удаление рассылок"""
    model = MailingSettings
    success_url = reverse_lazy('mailing:list_settings')

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.user != self.request.user:
            raise Http404
        return self.object
