from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication
from rest_framework import exceptions


class SettingsTokenAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        if key == settings.API_TOKEN:
            return AnonymousUser, key
        else:
            raise exceptions.AuthenticationFailed(_("Invalid token."))
