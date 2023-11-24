from django import template

register = template.Library()

@register.simple_tag
def calculate_percentage(count, total):
    return (count / total) * 100 if total else 0