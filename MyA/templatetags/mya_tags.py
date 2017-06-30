from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, urlname):
    """
    Return an string 'active' if current page matches given urlname.
    Can be used to set an active css class to the link of a current page.
    """
    if context.request.resolver_match.url_name == urlname:
        return 'active'
    return ''
