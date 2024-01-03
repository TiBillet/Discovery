from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

#Creating the User Class in case we'll need one in the future
class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True)


# The class where we'll stock the url's, pin code's and the rsa crypto of the server
class PrimaryLink(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    pin_code = models.CharField(max_length=8, unique=True, verbose_name="Le Code Pin")
    server_url = models.URLField(max_length=200, unique=True, verbose_name="Le lien du serveur")
    rsa_code_crypto = models.CharField(max_length=150, unique=True, blank=True, null=True, verbose_name="Le crypto code RSA")
