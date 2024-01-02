from django.shortcuts import render
from .models import PrimaryLink
import json
from django.http import JsonResponse

# from the url the function will get the pin and will elaborate it
# to get the url from the data and will send a json with the url
def send_url_based_on_pin(request, pin_link):
    primary_link = PrimaryLink.objects.get(server_url=pin_link)
    data = []
    data.append({
        'url': primary_link.server_url
    })
    return JsonResponse(data, safe=False)
