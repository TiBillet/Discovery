from .models import PrimaryLink
from rest_framework import serializers


# Validation of the pin code
class PinValidator(serializers.Serializer):
    pinCode = serializers.IntegerField(required=True)
    #check if the primary_link object exists
    def validate_pin_code(self, value):
        try:
            primary_link = PrimaryLink.objects.get(server_url=value)

        except PrimaryLink.DoesNotExist:
            raise serializers.ValidationError("The pin doesn't exist")

        return primary_link.server_url
