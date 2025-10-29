"""
Context processors to make custom variables available in all templates
"""
from django.conf import settings


def rtl_support(request):
    """
    Add RTL language support information to template context.
    This allows templates to check if the current language is RTL.
    
    Usage: Add 'language_manager.context_processors.rtl_support' to TEMPLATES context_processors
    """
    return {
        'RTL_LANGUAGES': getattr(settings, 'RTL_LANGUAGES', []),
    }

