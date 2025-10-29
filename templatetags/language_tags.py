"""
Custom template tags for language switching
"""
from django import template
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def change_language_url(context, language_code):
    """
    Returns the URL for the current page in the specified language.
    
    Usage in templates:
        {% load language_tags %}
        <a href="{% change_language_url 'ar' %}">العربية</a>
    
    Example: Converts /en/jobs/ to /ar/jobs/
    """
    request = context.get('request')
    if request:
        path = request.get_full_path()
        return translate_url(path, language_code)
    return f'/{language_code}/'

