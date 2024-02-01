from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from mailing.forms import ClientForm, MailingMessageForm, MailingSettingsForm, ModeratorMailingSettingsForm
from mailing.models import Client, MailingMessage, MailingSettings


class HomepageView(TemplateView):
    template_name = 'mailing/index.html'


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        queryset = super().get_queryset().filter()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:list_client')


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:list_client')


class MailingMessageListView(ListView):
    model = MailingMessage



    def get_queryset(self):
        queryset = super().get_queryset().filter()
        if self.request.user.groups.filter(name='mailing_mod').exists():
            return queryset
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MailingMessageCreateView(CreateView):
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
    model = MailingMessage



class MailingMessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:list_message')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user:
            raise Http404
        return self.object


class MailingSettingsListView(ListView):
    model = MailingSettings

    def get_queryset(self):
        queryset = super().get_queryset().filter()
        if self.request.user.groups.filter(name='mailing_mod').exists():
            return queryset
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

        return queryset


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:list_settings')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:list_settings')

    def get_form_class(self):
        if self.object.user == self.request.user:
            return MailingSettingsForm
        if self.request.user.groups.filter(name='mailing_mod').exists():
            return ModeratorMailingSettingsForm


class MailingSettingsDetailView(DetailView):
    model = MailingSettings


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:list_settings')

    def get_object(self, queryset=None):
        self.object = super().get_object()
        if self.object.user != self.request.user:
            raise Http404
        return self.object
