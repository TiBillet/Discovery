from django.test import TestCase
from primary_server_core.models import PrimaryLink


# Creating the PrimaryLink test clasx
class PrimaryLink(TestCase):
    def setUp(self):
        pass
        #self.primary_link = PrimaryLink.objects.create(pin_code="789112", server_url="https://tibillet.org")


    # Testing primarylink
    def test_primary_link(self):
       pass
       #self.assertEqual(self.primary_link.pin_code, '789112')
