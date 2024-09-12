from rest_framework import serializers

from .models import Customer, Policy


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "date_of_birth",
            "gender",
        ]
        read_only_fields = ["id"]


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = [
            "id",
            "policy_number",
            "customer",
            "policy_type",
            "premium_amount",
            "coverage_amount",
            "start_date",
            "end_date",
            "status",
            "is_accepted",
        ]
        read_only_fields = ["id", "premium_amount", "policy_number", "end_date"]

    def update(self, instance, validated_data):
        # Mark the policy as accepted and change status to 'active'
        if validated_data.get("is_accepted", instance.is_accepted):
            instance.is_accepted = True
            instance.status = Policy.PolicyStatus.ACTIVE

        instance.save()
        return instance
