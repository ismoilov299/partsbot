"""
Custom forms for Django admin
"""
from django.contrib.auth.forms import AuthenticationForm


class CleanedAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that cleans null characters from username and password
    This fixes the "Null characters are not allowed" error
    """
    
    def clean_username(self):
        """Clean null characters from username"""
        username = self.cleaned_data.get('username', '')
        if username and isinstance(username, str):
            # Remove null characters
            username = username.replace('\x00', '').strip()
        return username
    
    def clean(self):
        """Clean the entire form, including password"""
        # Get username and password from form data before validation
        username = self.data.get('username', '')
        password = self.data.get('password', '')
        
        # Clean null characters from raw data
        if username and isinstance(username, str) and '\x00' in username:
            # Create mutable copy and clean
            data = self.data.copy()
            data['username'] = username.replace('\x00', '').strip()
            self.data = data
        
        if password and isinstance(password, str) and '\x00' in password:
            # Create mutable copy and clean
            data = self.data.copy()
            data['password'] = password.replace('\x00', '').strip()
            self.data = data
        
        # Call parent clean method
        cleaned_data = super().clean()
        
        # Double check and clean password in cleaned_data
        if 'password' in cleaned_data:
            password = cleaned_data['password']
            if password and isinstance(password, str):
                cleaned_data['password'] = password.replace('\x00', '').strip()
        
        return cleaned_data

