
import requests

from django.conf import settings
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Client
from .utils import get_public_key, verify_signature

import logging
logger = logging.getLogger(__name__)


# Validation of the pin code
class PinValidator(serializers.Serializer):
    pin_code = serializers.CharField(max_length=6, min_length=6)

    # signature = serializers.CharField(max_length=512)
    # public_pem = serializers.CharField(max_length=512)
    #
    # def validate_signature(self, value):
    #     if not self.initial_data.get('public_pem'):
    #         raise serializers.ValidationError("Public pem not sended")
    #
    #     try:
    #         public_key = get_public_key(self.initial_data.get('public_pem'))
    #         if public_key.key_size < 2048:
    #             raise serializers.ValidationError("Public key size too small")
    #     except Exception as e:
    #         raise serializers.ValidationError("Public key not valid, must be 2048 min rsa key")
    #
    #     is_valid = verify_signature(public_key, self.initial_data.get('pin_code').encode('utf-8'), value)
    #     if not is_valid:
    #         raise serializers.ValidationError("Signature not valid")
    #     print(f"signature is_valid : {is_valid}")
    #     return value


    def validate(self, attrs):
        client = get_object_or_404(Client, pin_code=attrs.get('pin_code'))

        # Si le code a déja été réclamé, on envoie bouler. Sauf si on est en mode DEBUG
        if client.claimed_at and not settings.DEBUG:
            raise serializers.ValidationError("Client already claimed")

        self.client = client
        return attrs


class NewServerValidator(serializers.Serializer):
    url = serializers.URLField(max_length=200)
    public_pem = serializers.CharField(max_length=512)
    locale = serializers.CharField(max_length=2)

    def validate_public_pem(self, value):
        try:
            public_key = get_public_key(value)
            if public_key.key_size < 2048:
                raise serializers.ValidationError("Public key size too small")
        except Exception as e:
            raise serializers.ValidationError("Public key not valid, must be 2048 min rsa key")

        print(f"public_key is_valid")
        self.sended_public_key = public_key
        return value

    def validate(self, attrs):
        # Récupération de la clé validée dans validate_public_pem
        sended_public_key = self.sended_public_key

        try :
            # On fait une requete au serveur pour valider la clé
            confirmation = requests.get(f"{attrs['url']}/api/signed_key/", verify=(not settings.DEBUG))
            if confirmation.status_code != 200:
                raise serializers.ValidationError("URL Server not valid, confirmation request not reached")

            # La requete est ok, on parse et on vérifie la donnée envoyée
            data = confirmation.json()
            confirmation_public_pem = get_public_key(data.get('public_pem'))
        except Exception as e :
            raise serializers.ValidationError(f"URL Server not valid, confirmation request not reached : {e}")


        # Vérification de la clé envoyé par le serveur et la clé envoyé par le lien de vérification
        # De cette façon, on vérifie l'url du serveur. La demande correspond bien à un serveur hebergé sur ce DNS.
        if not confirmation_public_pem.public_numbers() == sended_public_key.public_numbers():
            raise serializers.ValidationError("Pub Key from confirmation cashless not valid")

        # Vérification de la signature envoyé lors de la demande de confirmation
        is_valid = verify_signature(sended_public_key, data.get('public_pem').encode('utf-8'), data.get('signature'))
        if not is_valid:
            raise serializers.ValidationError("Signature not valid")

        return attrs


class NewClientValidator(serializers.Serializer):
    client_name = serializers.CharField(max_length=200, required=True)
