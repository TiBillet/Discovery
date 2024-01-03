from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('<pin_link>', views.send_url_based_on_pin, name='pin_link'),
]

'''
return_status = 400
    if request.method == 'POST':
        json_data = json.loads(request.body)
        return_status = 200
    try:
        data = json_data['pinCode']
    except KeyError:
        print("nothing")
        #HttpResponseServerError("Malformed data!")
    #HttpResponse("Got json data")

    print(f"Data = {data}")
'''