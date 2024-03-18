import datetime
from django.core.cache import cache
from django.conf import settings
from rest_framework.authtoken.models import Token


class ActiveUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION')
        if header_token:
            token = header_token[6:]
            try:
                token_obj = Token.objects.get(key=token)
                current_user = token_obj.user
                now = datetime.datetime.now()
                cache.set(f'seen_{current_user.id}', now, settings.USER_LASTSEEN_TIMEOUT)
            except Token.DoesNotExist:
                pass

        response = self.get_response(request)

        return response
