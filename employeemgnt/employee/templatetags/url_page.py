from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.copy()
    for key in kwargs:
        query[key] = kwargs[key]
    return query.urlencode()
