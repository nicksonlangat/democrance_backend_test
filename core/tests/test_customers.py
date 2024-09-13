from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Customer


class CustomerApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_create_url = reverse("customer-create")
        self.customer_list_url = reverse("customer-list")

        self.customer_one = Customer.objects.create(
            first_name="Stewie",
            last_name="Griffin",
            email="stewie@gmail.com",
            phone_number="0718905654",
            date_of_birth="1992-01-01",
        )
        self.customer_two = Customer.objects.create(
            first_name="Meg",
            last_name="Quagmire",
            email="meg@gmail.com",
            phone_number="0726905654",
            date_of_birth="1970-01-01",
        )

    def test_create_customer_with_valid_data(self):
        """Test creating a customer with all required fields."""

        data = {
            "first_name": "Peter",
            "last_name": "Griffin",
            "email": "peter@gmail.com",
            "phone_number": "0720754946",
            "date_of_birth": "1995-06-12",
            "gender": Customer.Gender.MALE,
        }

        response = self.client.post(self.customer_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 3)
        self.assertEqual(Customer.objects.first().gender, "male")

    def test_create_customer_missing_fields(self):
        """Test creating a customer with missing required fields."""

        data = {"first_name": "Chris", "last_name": "Griffin"}

        response = self.client.post(self.customer_create_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("phone_number", response.data)
        self.assertIn("date_of_birth", response.data)

    def test_list_all_customers(self):
        """Test that all customers are returned when no filters are applied."""

        response = self.client.get(self.customer_list_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_by_first_name(self):
        """Test that customers can be filtered by first name."""

        response = self.client.get(self.customer_list_url, {"first_name": "Stewie"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["first_name"], "Stewie")

    def test_filter_by_last_name(self):
        """Test that customers can be filtered by last name."""

        response = self.client.get(self.customer_list_url, {"last_name": "Quagmire"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["last_name"], "Quagmire")

    def test_filter_by_date_of_birth(self):
        """Test that customers can be filtered by date of birth."""

        response = self.client.get(
            self.customer_list_url, {"date_of_birth": "1970-01-01"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["date_of_birth"], "1970-01-01")

    def test_filter_by_email(self):
        """Test that customers can be filtered by email."""

        response = self.client.get(
            self.customer_list_url, {"email": "stewie@gmail.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["email"], "stewie@gmail.com")

    def test_filter_by_multiple_parameters(self):
        """Test that customers can be filtered by multiple parameters at once."""

        response = self.client.get(
            self.customer_list_url, {"first_name": "Meg", "last_name": "Quagmire"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["first_name"], "Meg")

    def test_no_customers_found(self):
        """Test that an empty list is returned if no customers match the filters."""

        response = self.client.get(self.customer_list_url, {"first_name": "Joe"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
