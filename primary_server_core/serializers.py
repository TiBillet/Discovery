
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
    pin_code = serializers.CharField(max_length=8, min_length=6, required=True)
    client_rsa_pub_pem = serializers.CharField(max_length=512, required=False)
    client_name = serializers.CharField(max_length=200, required=False)

    def validate_client_rsa_pub_pem(self, value):
        try:
            pub = get_public_key(value)
            if pub.key_size < 2048:
                raise serializers.ValidationError("Public key size too small")
        except Exception as e:
            raise serializers.ValidationError("Public key not valid, must be 2048 min rsa key")
        return value

    def validate(self, attrs):
        client = get_object_or_404(Client, pin_code=attrs.get('pin_code'))

        if attrs.get('rsa_pub_pem') and attrs.get('client_name'):
            client.rsa_pub_pem = attrs['client_rsa_pub_pem']
            client.name = attrs['client_name']

        self.client = client
        return attrs


class NewServerValidator(serializers.Serializer):
    server_url = serializers.URLField(max_length=200, required=True)
    server_rsa_pub_pem = serializers.CharField(max_length=512, required=True)
    locale = serializers.CharField(max_length=2, required=True)

    def validate_server_rsa_pub_pem(self, value):
        try:
            pub = get_public_key(value)
            if pub.key_size < 2048:
                raise serializers.ValidationError("Public key size too small")
        except Exception as e:
            raise serializers.ValidationError("Public key not valid, must be 2048 min rsa key")

        return value

    def validate(self, attrs):
        # On fait une requete au serveur pour valider la clé
        confirmation = requests.get(f"{attrs['server_url']}/api/signed_key/", verify=(not settings.DEBUG))
        if confirmation.status_code != 200:
            raise serializers.ValidationError("Server not valid")

        data = confirmation.json()
        confirmation_public_pem = get_public_key(data.get('public_pem'))
        sended_public_pem = get_public_key(attrs.get('server_rsa_pub_pem'))
        if not confirmation_public_pem.public_numbers() == sended_public_pem.public_numbers():
            raise serializers.ValidationError("Pub Key from confirmation cashless not valid")

        is_valid = verify_signature(confirmation_public_pem, data.get('public_pem').encode('utf-8'), data.get('signature'))
        if not is_valid:
            raise serializers.ValidationError("Signature not valid")

        return attrs


class NewClientValidator(serializers.Serializer):
    client_name = serializers.CharField(max_length=200, required=True)
