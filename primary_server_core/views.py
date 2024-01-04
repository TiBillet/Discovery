from .models import PrimaryLink
from . serializers import PinValidator
import json, requests
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


# from the url the function will get the pin and will elaborate it
# to get the url from the data and will send a json with the url
#@csrf_exempt
@api_view(['POST'])
def send_url_based_on_pin(request):
    # passing the pin code to the Validator
    pin_code_validator = PinValidator(data=request.data)
    # checking if the pin code is correct
    if not pin_code_validator.is_valid():
        return Response({'message': "Code Pin Incorrect"}, status=status.HTTP_404_NOT_FOUND)

    # Get the url server link
    primary_link = pin_code_validator.validated_data
    return Response({'message': 'Code Pin Correct', 'url': primary_link}, status=status.HTTP_200_OK)
