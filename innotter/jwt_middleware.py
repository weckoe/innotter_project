import jwt

from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user

from innotter.settings import JWT_SECRET
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.get_full_path() != "/login/" and request.get_full_path() != "/refresh/":
            user = get_user(request)

            if user.is_authenticated:
                return user
            jwt_token = request.META.get('HTTP_AUTHORIZATION', None)
            if jwt_token:

                payload = jwt.decode(jwt_token.replace("Token ", ""), JWT_SECRET, algorithms=['HS256'])

                try:
                    User.objects.get(id=payload["user_id"])
                    return None

                except Exception as e:
                    return HttpResponse(f"Error: {e}")
            return HttpResponse("No JWT token provided")
        return None

