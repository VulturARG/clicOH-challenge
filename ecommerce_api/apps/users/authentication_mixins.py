from typing import Optional, Tuple

from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework.request import Request

from apps.users.authentication import ExpiringTokenAuthentication
from apps.users.models import User


class Authentication(authentication.BaseAuthentication):

    def get_user(self, request: Request) -> Optional[User]:
        token = get_authorization_header(request).split()
        if not token:
            return None

        try:
            token = token[1].decode()
        except IndexError:
            return None

        token_expire = ExpiringTokenAuthentication()
        user = token_expire.authenticate_credentials(token)

        if user is None:
            return None

        return user

    def authenticate(self, request: Request) -> Tuple[User, int]:
        user = self.get_user(request)
        if user is None:
            raise exceptions.AuthenticationFailed('credentials not sent')

        return user, 1
