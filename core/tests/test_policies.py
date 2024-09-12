from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Customer, Policy


class PolicyApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.customer = Customer.objects.create(
            first_name="Brian",
            last_name="Griffin",
            email="brian@gmail.com",
            phone_number="0728905654",
            date_of_birth="1990-01-01",
        )

        self.quote = Policy.objects.create(
            customer=self.customer,
            policy_type="motor",
            coverage_amount=10000,
            start_date=datetime.strptime("2024-09-12", "%Y-%m-%d").date(),
        )
        self.update_quote_url = reverse("quote-update", kwargs={"pk": self.quote.id})

        self.create_quote_url = reverse("quote")

    def test_create_policy_with_valid_data(self):
        data = {
            "customer": self.customer.id,
            "policy_type": "health",
            "coverage_amount": "30000000",
            "start_date": "2024-01-01",
        }

        response = self.client.post(self.create_quote_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Policy.objects.filter(policy_type="health").count(), 1)
        policy = Policy.objects.filter(policy_type="health").last()
        self.assertEqual(policy.customer, self.customer)
        self.assertEqual(policy.policy_type, "health")
        self.assertEqual(str(policy.premium_amount), "1650000.00")
        self.assertEqual(policy.status, "quoted")
        self.assertFalse(policy.is_accepted)

    def test_create_policy_with_missing_fields(self):
        data = {
            "customer": self.customer.id,
            "policy_type": "motor",
        }

        response = self.client.post(self.create_quote_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("coverage_amount", response.data)

    def test_accept_quote_and_mark_active(self):
        response = self.client.patch(self.update_quote_url, {"is_accepted": True})
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()
        self.assertTrue(self.quote.is_accepted)
        self.assertEqual(self.quote.status, "active")
