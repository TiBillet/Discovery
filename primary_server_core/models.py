from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

#Creating the User Class in case we'll need one in the future
class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True)

# The class where we'll stock the url's, pin code's and the rsa crypto of the server
class PrimaryLink(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    pin_code = models.CharField(max_length=8, unique=True, verbose_name="Code")
    server_url = models.URLField(max_length=200, unique=True, verbose_name="Url server")
    rsa_pub_pem = models.CharField(max_length=512, unique=True, blank=True, null=True, verbose_name="RSA public pem key")
    locale = models.CharField(max_length=2, default='en', verbose_name="Locale")