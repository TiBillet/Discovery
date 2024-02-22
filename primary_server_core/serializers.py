from rest_framework.generics import get_object_or_404

from .models import PrimaryLink
from rest_framework import serializers


# Validation of the pin code
class PinValidator(serializers.Serializer):
    pin_code = serializers.CharField(max_length=8, min_length=6, required=True)

    #check if the primary_link object exists
    def validate_pinCode(self, value):
        self.link = get_object_or_404(PrimaryLink, pin_code=value)
        return value


