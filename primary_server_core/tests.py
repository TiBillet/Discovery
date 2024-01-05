from django.test import TestCase
from primary_server_core.models import PrimaryLink, CustomUser


# Creating the PrimaryLink test clasx
class PrimaryLinkCase(TestCase):
    # creating a primary_link object
    def setUp(self):
        PrimaryLink.objects.create(pin_code="789112", server_url="https://tibillet.org/")

    # Testing primarylink
    def test_primary_link(self):
        pin1 = PrimaryLink.objects.get(pin_code='789112')
        # Testing when the code and the server url is right
        self.assertEqual(pin1.pin_code, '789112')
        self.assertEqual(pin1.server_url, 'https://tibillet.org/')
        # testing when the pin code and the server_url is wrong
        self.assertNotEquals(pin1.pin_code, '123456')
        self.assertNotEquals(pin1.server_url, 'https://yahoo.com/')

# Testing the POST méthod:
class TestCaseForm(TestCase):
    # launching setUp
    def setUp(self):
        PrimaryLink.objects.create(pin_code="789112", server_url="https://tibillet.org/")


    # creating the method that will test the POST
    def test_post(self):
        pass
