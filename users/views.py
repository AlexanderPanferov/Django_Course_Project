import random
import secrets
import string

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from users.models import User
from users.services import send_new_password, send_verification_link


class LoginView(BaseLoginView):
    """Страница входа"""
    form_class = UserLoginForm
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    """Страница выхода"""
    pass


class RegisterView(CreateView):
    """Страница регистрации"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Отправления ссылки для подтверждения регистрации"""
        verification_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        form.verification_code = verification_code
        user = form.save()
        user.verification_code = verification_code
        send_verification_link(user.email, verification_code)
        return super().form_valid(form)


class ProfileDeleteView(DeleteView):
    """Страница удаления профиля"""
    model = User
    success_url = reverse_lazy('mailing:mailing')


def verify(request):
    code = int(request.GET.get('code'))
    user = User.objects.get(verification_code=code)
    user.verified = True
    user.save()
    return render(request, 'users/verify.html')


class ProfileView(UpdateView):
    """Страница профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    """Генерация пароля"""
    new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('users:login'))
