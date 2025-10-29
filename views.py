"""
Language switching view
"""
from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect


@require_POST
@csrf_protect
def set_language(request):
    """
    Handle language switching with proper Django i18n support.
    Changes the URL to include the language prefix (e.g., /en/, /ar/)
    """
    from django.urls import translate_url
    
    language = request.POST.get('language')
    
    # Validate language code
    if language and language in dict(settings.LANGUAGES).keys():
        # Activate the language for this session
        translation.activate(language)
        # Use the string constant directly for Django 5.2 compatibility
        request.session['_language'] = language
        
        # Get the current path and translate it to the new language
        next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', '/')
        
        # Extract the path from the full URL if it's a full URL
        if next_url.startswith('http'):
            from urllib.parse import urlparse
            parsed = urlparse(next_url)
            next_url = parsed.path
        
        # Translate the URL to include the new language prefix
        try:
            next_url = translate_url(next_url, language)
        except:
            # If translation fails, default to the landing page with language prefix
            next_url = f'/{language}/'
        
        response = HttpResponseRedirect(next_url)
        
        # Set language cookie for persistence
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            language,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
        return response
    
    # If invalid language, just redirect back
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

