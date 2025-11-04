from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Two numbers multiply."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
