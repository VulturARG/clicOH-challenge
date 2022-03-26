from rest_framework import status, authentication, exceptions
from rest_framework.authentication import get_authorization_header

from apps.users.authentication import ExpiringTokenAuthentication


class Authentication(authentication.BaseAuthentication):
    user = None

    def get_user(self, request):
        """
        Return:
            * user      : User Instance or
            * message   : Error Message or
            * None      : Corrupt Token
        """
        token = get_authorization_header(request).split()
        print(token)
        print(type(token))

        return None

        # if not token:
        #     return None
        #
        # try:
        #     token = token[1].decode()
        # except:
        #     return None
        #
        # token_expire = ExpiringTokenAuthentication()
        # user = token_expire.authenticate_credentials(token)
        #
        # if user is None:
        #     return None

        self.user = user
        return user

    def authenticate(self, request):
        self.get_user(request)
        if self.user is None:
            raise exceptions.AuthenticationFailed('credentials not sent.')

        return self.user, 1
