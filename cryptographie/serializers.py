from .models import PrimaryLink
from rest_framework import serializers


# Validation of the pin code
class PinValidator(serializers.Serializer):
    pinCode = serializers.IntegerField(required=True)

    #check if the primary_link object exists
    def validate_pinCode(self, value):
        try:
            str_value = str(value)
            primary_link = PrimaryLink.objects.get(pin_code=value)
            return primary_link.server_url
        except PrimaryLink.DoesNotExist:
            raise serializers.ValidationError("The pin doesn't exist")

