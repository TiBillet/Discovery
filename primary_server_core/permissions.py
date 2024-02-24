import typing

from django.http import HttpRequest
from rest_framework_api_key.permissions import BaseHasAPIKey

from primary_server_core.models import ServerAPIKey
import logging
logger = logging.getLogger(__name__)


class HasAPIKey(BaseHasAPIKey):
    model = ServerAPIKey

    def get_key(self, request: HttpRequest) -> typing.Optional[str]:
        return super().get_key(request)

    def has_permission(self, request: HttpRequest, view: typing.Any) -> bool:
        # Récupération de la clé API qui va nous permettre de connaitre
        # le lieu et sa clé RSA publique pour vérifier la signature.
        key = self.get_key(request)
        if not key:
            logger.debug(f"HasAPIKey : no key")
            return False

        try :
            api_key: ServerAPIKey = self.model.objects.get_from_key(key)
            server = api_key.server
            request.server = server
            return super().has_permission(request, view)
        except ServerAPIKey.DoesNotExist:
            logger.warning(f"HasAPIKey : no api key")
            return False
        except Exception as e:
            logger.error(f"HasAPIKey : {e}")
            raise e

