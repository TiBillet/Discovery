from django.urls import path
from . import views

urlpatterns = [
    path('pin_code/', views.pin_code, name='pin_code'),
    path('new_server/', views.new_server, name='new_server'),
    path('new_client/', views.new_client, name='new_client'),

]
