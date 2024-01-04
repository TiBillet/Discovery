from django.shortcuts import render, redirect
from .models import PrimaryLink
from . serializers import PinValidator
import json, requests
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
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
    return_status = 200
    message = f"Code pin correct"
    if request.method == 'POST':
        # passing the pin code to the Validator
        pin_code_validator = PinValidator(data=request.data)
        #checking if the pin code is correct
        if not pin_code_validator.is_valid():
            print(" Wrong pin")
            return HttpResponseBadRequest("Code pin incorrect")

    # Get the url server link
    primary_link = pin_code_validator.validated_data
    print('The pin code', primary_link)

    #primary_link = pin_validate.validated_data.get('pin_link')
    data = {}
    data['url'] = primary_link
    data['return_status'] = return_status
    data['message'] = message

    return JsonResponse(data, safe=False)
