from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from pytils.translit import slugify
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForms
from blog.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogDetailView(DetailView):
    """Отображения страницы блога"""
    model = Blog
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        """Реализация счетчика просмотров"""
        slug = self.kwargs.get('slug')
        blog = self.model.objects.get(slug=slug)
        blog.view_count += 1
        blog.save()
        return blog


class BlogCreateView(LoginRequiredMixin, CreateView):
    """Создание блога"""
    model = Blog
    form_class = BlogForms
    success_url = reverse_lazy('blog:list_blog')

    def get_form_class(self):
        if not self.request.user.groups.filter(name='blog_mod').exists():
            raise Http404
        return BlogForms

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save()
            blog.slug = slugify(blog.title)
            blog.save()
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование блога"""
    model = Blog
    form_class = BlogForms
    success_url = reverse_lazy('blog:list_blog')

    def get_form_class(self):
        if not self.request.user.groups.filter(name='blog_mod').exists():
            raise Http404
        return BlogForms


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление блога"""
    model = Blog
    success_url = reverse_lazy('blog:list_blog')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if not self.request.user.groups.filter(name='blog_mod').exists():
            raise Http404
        return self.object
