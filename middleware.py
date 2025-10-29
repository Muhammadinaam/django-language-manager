"""
API Language Middleware
Handles language switching for API requests using HTTP headers
"""
from django.utils import translation
from django.conf import settings


class APILanguageMiddleware:
    """
    Middleware to handle language switching for API requests.
    Checks for language in:
    1. X-Language custom header
    2. Accept-Language standard header
    3. Falls back to default language
    
    Usage: Add to MIDDLEWARE in settings.py
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply to API routes
        if request.path.startswith('/api/'):
            # Check for custom X-Language header
            language = request.META.get('HTTP_X_LANGUAGE')
            
            # Fall back to Accept-Language header
            if not language:
                accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
                if accept_language:
                    # Parse Accept-Language header (e.g., "ar, en;q=0.9")
                    language = accept_language.split(',')[0].strip().split(';')[0].strip()
            
            # Validate and activate language
            supported_languages = dict(settings.LANGUAGES).keys()
            if language and language in supported_languages:
                translation.activate(language)
                request.LANGUAGE_CODE = language
        
        response = self.get_response(request)
        return response

