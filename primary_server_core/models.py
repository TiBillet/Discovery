from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey


# Creating the User Class in case we'll need one in the future
class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True)


# The class where we'll stock the url's, pin code's and the rsa crypto of the server
class CashlessServer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    server_url = models.URLField(max_length=200, unique=True, verbose_name="Url server")
    server_rsa_pub_pem = models.CharField(max_length=512, unique=True, blank=True, null=True,
                                          verbose_name="RSA public pem key")
    locale = models.CharField(max_length=2, default='en', verbose_name="Locale")

    def __str__(self):
        return f"{self.server_url}"


class Client(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=100)
    rsa_pub_pem = models.CharField(max_length=512, unique=True, blank=True, null=True,
                                   verbose_name="RSA public pem key")
    pin_code = models.PositiveIntegerField(max_length=8, unique=True, blank=True, null=True)
    cashless_server = models.ForeignKey(CashlessServer, on_delete=models.CASCADE, related_name='clients')


class ServerAPIKey(AbstractAPIKey):
    server = models.ForeignKey(
        CashlessServer,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "API key"
        verbose_name_plural = "API keys"
