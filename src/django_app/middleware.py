"""
Custom middleware to clean null characters from request data
"""
import re


def clean_null_characters(value):
    """Remove null characters from a string value"""
    if isinstance(value, str):
        return value.replace('\x00', '').strip()
    elif isinstance(value, list):
        return [clean_null_characters(v) for v in value]
    return value


class NullCharacterCleanerMiddleware:
    """
    Middleware to remove null characters from POST data
    This fixes the "Null characters are not allowed" error in Django admin login
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Clean null characters from POST data
        if request.method == 'POST':
            # Create a mutable copy of POST data
            post_data = request.POST.copy()
            cleaned = False
            
            # Clean all POST fields
            for key in list(post_data.keys()):
                value = post_data[key]
                if value and '\x00' in str(value):
                    # Remove null characters
                    cleaned_value = clean_null_characters(value)
                    if cleaned_value != value:
                        post_data[key] = cleaned_value
                        cleaned = True
            
            # Replace POST data if cleaned
            if cleaned:
                request.POST = post_data
        
        response = self.get_response(request)
        return response

