from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, urlname):
    if context.request.resolver_match.url_name == urlname:
        return 'active'
    return ''
