from django import template

register = template.Library()


@register.simple_tag()
def getEmployeeAddress(obj):
    return ''
    if obj.getEmployeeAddress():
        return obj.getEmployeeAddress().district
    else:
        pass
