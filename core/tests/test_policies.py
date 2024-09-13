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
        self.update_quote_url = reverse("quote-detail", kwargs={"pk": self.quote.id})

        self.create_quote_url = reverse("quote-create")
        self.policy_list_url = reverse("policy-list")

    def test_create_policy_with_valid_data(self):
        """
        Test that a policy can be created with valid fields.
        """
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

    def test_create_policy_with_missing_fields(self):
        """
        Test that a policy cannot be created without missing fields.
        """
        data = {
            "customer": self.customer.id,
            "policy_type": "motor",
        }

        response = self.client.post(self.create_quote_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("coverage_amount", response.data)

    def test_accept_quote(self):
        """
        Test that a policy status can change to accepted
        """
        response = self.client.patch(
            self.update_quote_url, {"status": Policy.PolicyStatus.ACCEPTED}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()

        self.assertEqual(self.quote.status, "accepted")

    def test_pay_quote(self):
        """
        Test that a policy status can change to active
        """
        response = self.client.patch(
            self.update_quote_url, {"status": Policy.PolicyStatus.ACTIVE}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quote.refresh_from_db()
        self.assertEqual(self.quote.status, "active")

    def test_list_all_policies(self):
        """
        Test that all policies are returned when no filters are applied.
        """

        response = self.client.get(self.policy_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_by_customer_id(self):
        """
        Test that policies are filtered by customer_id.
        """

        response = self.client.get(
            self.policy_list_url, {"customer_id": self.customer.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for policy in response.data:
            self.assertEqual(policy["customer"]["id"], self.customer.id)

    def test_filter_by_policy_type(self):
        """
        Test that policies are filtered by policy type.
        """

        response = self.client.get(self.policy_list_url, {"policy_type": "motor"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for policy in response.data:
            self.assertEqual(policy["policy_type"], "motor")

    def test_filter_by_policy_status(self):
        """
        Test that policies are filtered by policy status.
        """

        response = self.client.get(self.policy_list_url, {"policy_status": "quoted"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        for policy in response.data:
            self.assertEqual(policy["status"], "quoted")

    def test_filter_by_multiple_parameters(self):
        """
        Test that policies are filtered by multiple parameters (customer_id, policy_status).
        """

        response = self.client.get(
            self.policy_list_url,
            {"customer_id": self.customer.id, "policy_type": "motor"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["policy_type"], "motor")

    def test_no_policies_found(self):
        """
        Test that no policies are returned if none match the filters.
        """

        response = self.client.get(self.policy_list_url, {"policy_type": "new"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_policy_history(self):
        """
        Test that the policy history is returned for a given policy.
        """
        url = reverse("policy-history", kwargs={"pk": self.quote.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["status"], "quoted")
