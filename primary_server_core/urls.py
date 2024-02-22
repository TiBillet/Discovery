from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('pin_code/', views.send_url_based_on_pin, name='pin_code'),
    path('new_server/', views.create_link, name='pin_code'),
]
