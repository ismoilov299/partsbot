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
    Only processes admin login requests and only cleans username/password fields
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Only process POST requests to admin login
        if request.method == 'POST' and request.path.startswith('/admin/login'):
            # Check if username or password fields have null characters
            has_null_chars = False
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            
            if username and '\x00' in username:
                has_null_chars = True
                logger.warning(f"Found null characters in username field")
            if password and '\x00' in password:
                has_null_chars = True
                logger.warning(f"Found null characters in password field")
            
            # Only modify if null characters are found
            if has_null_chars:
                # Create a mutable copy of POST data
                post_data = request.POST.copy()
                
                # Clean username
                if 'username' in post_data:
                    original = post_data['username']
                    post_data['username'] = clean_null_characters(post_data['username'])
                    if original != post_data['username']:
                        logger.info(f"Cleaned username field: removed null characters")
                
                # Clean password
                if 'password' in post_data:
                    original = post_data['password']
                    post_data['password'] = clean_null_characters(post_data['password'])
                    if original != post_data['password']:
                        logger.info(f"Cleaned password field: removed null characters")
                
                # Replace POST data - use _post to avoid re-parsing
                request._post = post_data
                # Also update the mutable POST
                request.POST = post_data
        
        response = self.get_response(request)
        return response

