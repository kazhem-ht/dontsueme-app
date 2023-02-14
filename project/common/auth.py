from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from pprint import pprint
import logging

class MyAuthenticationBackend(OIDCAuthenticationBackend):

    def get_username(self, claims):
        """Generate username based on claims."""
        return claims.get('preferred_username')
