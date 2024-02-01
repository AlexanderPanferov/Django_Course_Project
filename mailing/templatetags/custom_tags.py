from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, mailing_mod):
    return user.groups.filter(name=mailing_mod).exists()