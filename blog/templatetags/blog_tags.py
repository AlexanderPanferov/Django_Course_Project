from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, blog_mod):
    return user.groups.filter(name=blog_mod).exists()
