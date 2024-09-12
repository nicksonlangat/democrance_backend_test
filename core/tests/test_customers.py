from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Customer


class CustomerCreateApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_customer_url = reverse("customer-create")

    def test_create_customer_with_valid_data(self):
        data = {
            "first_name": "Peter",
            "last_name": "Griffin",
            "email": "peter@gmail.com",
            "phone_number": "0720754946",
            "date_of_birth": "1995-06-12",
            "gender": Customer.Gender.MALE,
        }

        response = self.client.post(self.create_customer_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().gender, "male")

    def test_create_customer_missing_fields(self):
        data = {"first_name": "Chris", "last_name": "Griffin"}

        response = self.client.post(self.create_customer_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("phone_number", response.data)
        self.assertIn("date_of_birth", response.data)
