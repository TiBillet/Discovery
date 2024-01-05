from .models import PrimaryLink
from rest_framework import serializers


# Validation of the pin code
class PinValidator(serializers.Serializer):
    pinCode = serializers.CharField(max_length=6, required=True)

    #check if the primary_link object exists
    def validate_pinCode(self, value):
        try:
            PrimaryLink.objects.get(pin_code=value)
            return value
        except PrimaryLink.DoesNotExist:
            raise serializers.ValidationError("The pin doesn't exist")
