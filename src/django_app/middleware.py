"""
Custom middleware to clean null characters from request data
"""
import logging

logger = logging.getLogger(__name__)


def clean_null_characters(value):
    """Remove null characters from a string value"""
    if isinstance(value, str):
        cleaned = value.replace('\x00', '')
        # Only strip if we actually removed something
        if cleaned != value:
            cleaned = cleaned.strip()
        return cleaned
    elif isinstance(value, list):
        return [clean_null_characters(v) for v in value]
    return value


class NullCharacterCleanerMiddleware:
    """
    Middleware to remove null characters from POST data
    This fixes the "Null characters are not allowed" error in Django admin login
    Processes all POST requests and cleans all fields that contain null characters
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process all POST requests
        if request.method == 'POST':
            # Check if any POST field has null characters
            has_null_chars = False
            
            # Check all POST fields for null characters
            for key in request.POST.keys():
                value = request.POST.get(key, '')
                if value and isinstance(value, str) and '\x00' in value:
                    has_null_chars = True
                    logger.warning(f"Found null characters in field: {key}")
                    break
            
            # Only modify if null characters are found
            if has_null_chars:
                # Create a mutable copy of POST data
                post_data = request.POST.copy()
                
                # Clean all POST fields
                for key in list(post_data.keys()):
                    value = post_data[key]
                    if value:
                        cleaned_value = clean_null_characters(value)
                        if cleaned_value != value:
                            post_data[key] = cleaned_value
                            logger.info(f"Cleaned field '{key}': removed null characters")
                
                # Replace POST data properly
                # Use _post to avoid re-parsing
                request._post = post_data
                # Update POST to use the cleaned data
                request.POST = post_data
        
        response = self.get_response(request)
        return response


class RemoveCOOPHeaderMiddleware:
    """
    Middleware to remove Cross-Origin-Opener-Policy header for HTTP
    This header requires HTTPS or localhost, so we remove it for HTTP
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Remove Cross-Origin-Opener-Policy header for HTTP
        # This header is only valid for HTTPS or localhost
        # Check if header exists and remove it
        if hasattr(response, 'headers'):
            # Django 3.2+ uses response.headers
            if 'Cross-Origin-Opener-Policy' in response.headers:
                del response.headers['Cross-Origin-Opener-Policy']
        elif hasattr(response, '_headers'):
            # Older Django versions use _headers dict
            coop_key = None
            for key in list(response._headers.keys()):
                if key.lower() == 'cross-origin-opener-policy':
                    coop_key = key
                    break
            if coop_key:
                del response._headers[coop_key]
        
        return response

