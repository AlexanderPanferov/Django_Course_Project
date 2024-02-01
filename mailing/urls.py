from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import HomepageView, ClientListView, ClientCreateView, ClientUpdateView, ClientDetailView, \
    ClientDeleteView, MailingMessageDeleteView, MailingMessageDetailView, MailingMessageUpdateView, \
    MailingMessageCreateView, MailingMessageListView, MailingSettingsDeleteView, MailingSettingsDetailView, \
    MailingSettingsUpdateView, MailingSettingsCreateView, MailingSettingsListView, MailingLogListView

app_name = MailingConfig.name

urlpatterns = [
    path('', HomepageView.as_view(), name='mailing'),
    path('client', cache_page(60)(ClientListView.as_view()), name='list_client'),
    path('client/create/', ClientCreateView.as_view(), name='create_client'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='edit_client'),
    path('client/detail/<int:pk>/', ClientDetailView.as_view(), name='view_client'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('message', cache_page(60)(MailingMessageListView.as_view()), name='list_message'),
    path('message/create/', MailingMessageCreateView.as_view(), name='create_message'),
    path('message/edit/<int:pk>/', MailingMessageUpdateView.as_view(), name='edit_message'),
    path('message/detail/<int:pk>/', MailingMessageDetailView.as_view(), name='view_message'),
    path('message/delete/<int:pk>/', MailingMessageDeleteView.as_view(), name='delete_message'),
    path('mailingsettings', MailingSettingsListView.as_view(), name='list_settings'),
    path('mailingsettings/create/', MailingSettingsCreateView.as_view(), name='create_settings'),
    path('mailingsettings/edit/<int:pk>/', MailingSettingsUpdateView.as_view(), name='edit_settings'),
    path('mailingsettings/detail/<int:pk>/', MailingSettingsDetailView.as_view(), name='view_settings'),
    path('mailingsettings/delete/<int:pk>/', MailingSettingsDeleteView.as_view(), name='delete_settings'),
    path('mailinglog/', MailingLogListView.as_view(), name='list_logs')
]


