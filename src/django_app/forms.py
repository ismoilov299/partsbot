"""
Custom forms for Django admin
"""
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class CleanedAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that cleans null characters from username and password
    This fixes the "Null characters are not allowed" error
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Clean null characters from raw data before validation
        if self.data:
            data = self.data.copy()
            
            # Clean username
            if 'username' in data:
                username = data['username']
                if username and isinstance(username, str) and '\x00' in username:
                    data['username'] = username.replace('\x00', '').strip()
            
            # Clean password
            if 'password' in data:
                password = data['password']
                if password and isinstance(password, str) and '\x00' in password:
                    data['password'] = password.replace('\x00', '').strip()
            
            self.data = data
    
    def clean_username(self):
        """Clean null characters from username"""
        username = super().clean_username()
        if username and isinstance(username, str):
            username = username.replace('\x00', '').strip()
        return username
    
    def clean(self):
        """Clean and authenticate"""
        # Call parent clean method - this will authenticate the user
        cleaned_data = super().clean()
        return cleaned_data

