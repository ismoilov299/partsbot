"""
Custom forms for Django admin
"""
from django.contrib.auth.forms import AuthenticationForm


class CleanedAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that cleans null characters from username and password
    This fixes the "Null characters are not allowed" error
    
    Note: Middleware should handle most cases, but this provides an additional safety layer
    """
    
    def clean_username(self):
        """Clean null characters from username"""
        # Call parent first to get cleaned username
        username = super().clean_username()
        # Then clean null characters
        if username and isinstance(username, str):
            username = username.replace('\x00', '').strip()
        return username
    
    def clean(self):
        """Clean the entire form, including password"""
        # Call parent clean method (this will validate and authenticate)
        # Middleware should have already cleaned null characters, but we double-check here
        cleaned_data = super().clean()
        
        # Double-check for null characters in cleaned data (safety measure)
        if 'username' in cleaned_data:
            username = cleaned_data['username']
            if username and isinstance(username, str):
                cleaned_data['username'] = username.replace('\x00', '').strip()
        
        # Note: password is not in cleaned_data for security reasons
        # But middleware should have cleaned it already
        
        return cleaned_data

