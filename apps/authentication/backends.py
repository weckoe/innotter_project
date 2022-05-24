import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from apps.authentication.models import User
from apps.authentication.jwt_constants import JWT_SECRET


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = "Token"

    def authenticate(self, request):

        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header and len(auth_header) != 2:
            return None

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        except Exception as e:
            print(e)
            msg = "Authentication error. Cannot decode token"
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload["user_id"])
        except User.DoesNotExist:
            msg = "User with this token not found."
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "Current user is not acitve."
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)

