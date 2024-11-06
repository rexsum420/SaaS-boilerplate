from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        try:
            token_obj = Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        return (token_obj.user, token)
