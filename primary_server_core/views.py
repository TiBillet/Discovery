import random

from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .models import CashlessServer, Client, ServerAPIKey
from .permissions import HasAPIKey
from .serializers import PinValidator, NewServerValidator, NewClientValidator
from .utils import hash_hexdigest, get_client_ip

import logging
logger = logging.getLogger(__name__)

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

    # return Response(data, status=status.HTTP_200_OK)
    # TODO: supprimer pour la prod
    return Response(data, headers={"Access-Control-Allow-Origin":"*"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def new_server(request):
    logger.info(f"new_server request received. Ip : {get_client_ip(request)}")
    new_server_validator = NewServerValidator(data=request.data)
    if not new_server_validator.is_valid():
        return Response(new_server_validator.errors, status=status.HTTP_400_BAD_REQUEST)
    validated_data = new_server_validator.validated_data
    logger.info(f"new_server request received. validated_data : {validated_data}")

    # L'url est stoquée chiffrée.
    # Pour faire une recherche, on la hash d'abord
    hashed_url = hash_hexdigest(validated_data['url'])
    logger.info(f"new_server request received. hashed_url : {hashed_url}")

    try :
        # The key and its signature have been validated.
        # We replace any old key if it exists
        server, created = CashlessServer.objects.get_or_create(hashed_url=hashed_url)
        # If the server already exists, we delete the old keys,
        # in the event of reinstallation or key change: The DNS has been validated by the confirmation request in the NewServerValidator.
        server.public_pem = validated_data['public_pem']
        server.api_keys.all().delete()
        server.set_url(validated_data['url'])
        server.save()
        logger.info(f"serveur {server} updated. Created : {created}")
    except Exception as e :
        logger.error(f"get_or_create try error : {e}")
        raise e


    try:
        # key create :
        enc_key, key = ServerAPIKey.objects.create_key(name=f"{hashed_url}", server=server)
        data = {
            "created": created,
            "key": key,
        }
        logger.info(f"Api Key created. return 201")
    except Exception as e:
        logger.error(f"api key creation : {e}")
        raise e
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
