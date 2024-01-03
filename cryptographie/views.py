from django.shortcuts import render, redirect
from .models import PrimaryLink
from . serializers import PinValidator
import json, requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# The home page will signal if the pin wasen't correct:
def home_page(request):
    message = "Le pin que vous avez entrez n'est pas correct"
    return render(request, 'general/home.html', {'message': message})

# from the url the function will get the pin and will elaborate it
# to get the url from the data and will send a json with the url
#@csrf_exempt
@api_view(['POST'])
def send_url_based_on_pin(request, pin_link):
    '''
    if request.method == 'POST':
        pin_validate = PinValidator(data=request.data)
    # send to home page if the pin is invalid
    if not pin_validate.is_valid():
        print("Not valid")
        return redirect('home_page')
    # Get the object if the pin is valid
    print("Valiiiiid")
    '''

    return_status = 200
    message = f"Code pin correct"
    if request.method == 'POST':
        json_data = json.loads(request.body)
    try:
        data = str(json_data['pinCode'])
    except KeyError:
        print("nothing")

    print(f"Data Type = {type(data)}")
    return_url = None
    try:
        primary_link = PrimaryLink.objects.get(pin_code=data)
        return_url = primary_link.server_url
    except PrimaryLink.DoesNotExist:
        return_status = 400
        message = f"Le code pin n'existe pas!"

    #primary_link = pin_validate.validated_data.get('pin_link')
    data = []
    data.append({
        'url': return_url,
        'return_status': return_status,
        'message': message
    })
    print(data)
    return JsonResponse(data, safe=False)
