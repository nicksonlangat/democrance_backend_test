import uuid
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from common.models import BaseModel

# Create your models here.


class Customer(BaseModel):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=250)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=10, choices=Gender.choices, null=True, blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Policy(BaseModel):
    class PolicyType(models.TextChoices):
        HEALTH = "health", "Health Insurance"
        LIFE = "life", "Life Insurance"
        MOTOR = "motor", "Motor Insurance"
        HOME = "home", "Home Insurance"

    class PolicyStatus(models.TextChoices):
        QUOTED = "quoted", "Quoted"
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        CANCELLED = "cancelled", "Cancelled"

    policy_number = models.CharField(max_length=100, unique=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="insurance_policies"
    )
    policy_type = models.CharField(max_length=20, choices=PolicyType.choices)
    premium_amount = models.DecimalField(
        max_digits=15, decimal_places=2, null=True, blank=True
    )
    coverage_amount = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    status = models.CharField(
        max_length=10, choices=PolicyStatus.choices, default=PolicyStatus.QUOTED
    )
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.policy_number} - {self.policy_type} for {self.customer}"

    def save(self, *args, **kwargs):
        if not self.policy_number:
            # automatically generate distinct policy numbers
            self.policy_number = str(uuid.uuid4()).replace("-", "").upper()[:10]

        if not self.end_date:
            # set the end_date, a year from the start date assuming a yearly coverage model
            self.end_date = self.start_date + timedelta(days=365)

        if not self.premium_amount:
            self.premium_amount = self.calculate_insurance_premium_amount()
        super(Policy, self).save(*args, **kwargs)

    @property
    def has_expired(self):
        """
        Check if a policy's duration has elapsed hence invalid/expired
        """
        now = timezone.now()

        return self.end_date <= now.date()

    def calculate_insurance_premium_amount(self):
        """
        This calculation is based on the policy type but can
        be extended to factor in other factors. It is extensible.
        """

        initial_rate = Decimal("0.05")  # i.e 5% (5/100), of coverage amount

        # Initial premium calculation assuming it is yearly
        premium_to_pay = initial_rate * self.coverage_amount

        match self.policy_type:
            case self.PolicyType.HEALTH:
                premium_to_pay *= Decimal("1.1")
            case self.PolicyType.LIFE:
                premium_to_pay *= Decimal("1.05")
            case self.PolicyType.MOTOR:
                premium_to_pay *= Decimal("1.2")
            case self.PolicyType.HOME:
                premium_to_pay *= Decimal("1.08")

        return premium_to_pay
