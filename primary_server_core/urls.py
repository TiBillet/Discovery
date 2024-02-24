from django.urls import path
from . import views

urlpatterns = [
    path('pin_code/', views.send_url_based_on_pin, name='pin_code'),
    path('new_server/', views.new_server, name='new_server'),
    path('new_client/', views.new_client, name='new_client'),

]
