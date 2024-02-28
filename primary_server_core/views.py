import random

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import CashlessServer, Client, ServerAPIKey
from .permissions import HasAPIKey
from .serializers import PinValidator, NewServerValidator, NewClientValidator
from .utils import rsa_encrypt_string, hash_hexdigest


# from the url the function will get the pin and will elaborate it
# to get the url from the data and will send a json with the server_url
# @csrf_exempt
@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def pin_code(request):
    # passing the pin code to the Validator
    pin_code_validator = PinValidator(data=request.data)
    # checking if the pin code is correct
    if not pin_code_validator.is_valid():
        # print("Decomposed pin_code ", pin_code_validator.errors['pinCode'][0])
        return Response(pin_code_validator.errors, status=status.HTTP_400_BAD_REQUEST)

    client: Client = pin_code_validator.client
    client.claimed_at = timezone.now()
    # client.rsa_pub_pem = pin_code_validator.validated_data['public_pem']
    client.save()

    server = client.cashless_server

    data = {
        "server_url": server.get_url(),
        "server_public_pem": server.public_pem,
        "locale": server.locale,
    }

    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def new_server(request):
    new_server_validator = NewServerValidator(data=request.data)
    if not new_server_validator.is_valid():
        return Response(new_server_validator.errors, status=status.HTTP_400_BAD_REQUEST)
    validated_data = new_server_validator.validated_data

    # L'url est stoquée chiffrée.
    # Pour faire une recherche, on la hash d'abord
    hashed_url = hash_hexdigest(validated_data['url'])

    # La clé et sa signature on été validée.
    # On remplace une eventuelle vieille clé si elle existe
    server, created = CashlessServer.objects.get_or_create(hashed_url=hashed_url)
    # Si le serveur existe déjà, on supprime les anciennes clés,
    # en cas de reinstallation ou de changement de clé
    # Le DNS a été validé par la requete de confirmation dans le validateur NewServerValidator
    server.public_pem = validated_data['public_pem']
    server.api_keys.all().delete()
    server.set_url(validated_data['url'])
    server.save()

    enc_key, key = ServerAPIKey.objects.create_key(name=f"{hashed_url}", server=server)
    data = {
        "created": created,
        "key": key,
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([HasAPIKey])
def new_client(request):
    new_client_validator = NewClientValidator(data=request.data)
    if new_client_validator.is_valid():
        validated_data = new_client_validator.validated_data
        serveur = request.server

        # # Génération du code pin
        pin_code = random.randint(100000, 999999)
        while Client.objects.filter(pin_code=pin_code).exists():
            pin_code = random.randint(100000, 999999)

        Client.objects.create(name=validated_data['client_name'],
                              cashless_server=serveur,
                              pin_code=pin_code)

        return Response({"pin_code": pin_code}, status=status.HTTP_201_CREATED)

    return Response(new_client_validator.errors, status=status.HTTP_400_BAD_REQUEST)
