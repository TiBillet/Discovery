from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

from primary_server_core.utils import get_public_key, fernet_encrypt, fernet_decrypt, hash_hexdigest


# Creating the User Class in case we'll need one in the future
class CustomUser(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    email = models.EmailField(max_length=100, unique=True)


# The class where we'll stock the url's, pin code's and the rsa crypto of the server
class CashlessServer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    hashed_url = models.CharField(max_length=512, unique=True, verbose_name="Hashed url server")
    url = models.URLField(max_length=512, unique=True, verbose_name="Encrypted url server")
    public_pem = models.CharField(max_length=512, unique=True, blank=True, null=True,
                                          verbose_name="RSA public pem key")
    locale = models.CharField(max_length=2, default='en', verbose_name="Locale")

    def __str__(self):
        return f"{self.url}"

    def set_hashed_url(self):
        self.hashed_url = hash_hexdigest(self.url)
        self.save()

    # On chiffre l'url avec fernet
    def set_url(self, url):
        self.url = fernet_encrypt(url)
        self.save()

    def get_url(self):
        return fernet_decrypt(self.url)



class Client(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=100)
    cashless_server = models.ForeignKey(CashlessServer, on_delete=models.CASCADE, related_name='clients')
    pin_code = models.PositiveIntegerField(unique=True, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    claimed_at = models.DateTimeField(blank=True, null=True)

    rsa_pub_pem = models.CharField(max_length=512, unique=True, blank=True, null=True,
                                   verbose_name="RSA public pem key")

    def get_public_key(self):
        return get_public_key(self.rsa_pub_pem)


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
