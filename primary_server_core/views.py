import random

from django.conf import settings
from rest_framework.throttling import AnonRateThrottle

from .models import PrimaryLink
from .serializers import PinValidator, LinkValidator
import json, requests
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes


# from the url the function will get the pin and will elaborate it
# to get the url from the data and will send a json with the server_url
# @csrf_exempt
@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def send_url_based_on_pin(request):
    # passing the pin code to the Validator
    pin_code_validator = PinValidator(data=request.data)
    # checking if the pin code is correct
    if not pin_code_validator.is_valid():
        # print("Decomposed pin_code ", pin_code_validator.errors['pinCode'][0])
        return Response(pin_code_validator.errors, status=status.HTTP_400_BAD_REQUEST)

    link: PrimaryLink = pin_code_validator.link
    data = {
        "server_url": link.server_url,
        "rsa_pub_pem": link.rsa_pub_pem,
        "locale": link.locale,
    }

    # send the server_url
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def create_link(request):
    new_link = LinkValidator(data=request.data)
    if not new_link.is_valid():
        return Response(new_link.errors, status=status.HTTP_400_BAD_REQUEST)
    validated_data = new_link.validated_data

    # Si on est en dev'/debug
    if settings.DEBUG:
        if PrimaryLink.objects.filter(server_url=validated_data['server_url']).exists():
            # update rsa key
            link = PrimaryLink.objects.get(server_url=validated_data['server_url'])
            link.rsa_pub_pem = validated_data['rsa_pub_pem']
            link.save()
            return Response({"pin_code": link.pin_code}, status=status.HTTP_201_CREATED)

    # Génération du code pin
    validated_data['pin_code'] = random.randint(100000, 999999)
    while PrimaryLink.objects.filter(pin_code=validated_data['pin_code']).exists():
        validated_data['pin_code'] = random.randint(100000, 999999)

    try :
        link = PrimaryLink.objects.create(**validated_data)
        return Response({"pin_code": link.pin_code}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)