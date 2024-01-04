from django.shortcuts import render, redirect
from .models import PrimaryLink
from . serializers import PinValidator
import json, requests
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# The home page will signal if the pin wasen't correct:
def home_page(request):
    message = "Le pin que vous avez entrez n'est pas correct"
    return render(request, 'general/home.html', {'message': message})

# from the url the function will get the pin and will elaborate it
# to get the url from the data and will send a json with the url
#@csrf_exempt
@api_view(['GET','POST'])
def send_url_based_on_pin(request):

    if request.method == 'POST':
        # passing the pin code to the Validator
        pin_code_validator = PinValidator(data=request.data)
        #checking if the pin code is correct
        if not pin_code_validator.is_valid():
            return HttpResponseBadRequest("Code pin incorrect")

    # Get the url server link
    primary_link = pin_code_validator.validated_data
    return Response(primary_link)
