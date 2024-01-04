from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('pin_code/', views.send_url_based_on_pin, name='pin_code'),
]
