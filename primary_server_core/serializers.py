from .models import PrimaryLink
from rest_framework import serializers


# Validation of the pin code
class PinValidator(serializers.Serializer):
    pinCode = serializers.CharField(max_length=8, min_length=6, required=True)

    #check if the primary_link object exists
    def validate_pinCode(self, value):
        try:
            self.server_url = PrimaryLink.objects.get(pin_code=value).server_url
            return value
        except PrimaryLink.DoesNotExist:
            raise serializers.ValidationError("Code Pin Incorrect.")
