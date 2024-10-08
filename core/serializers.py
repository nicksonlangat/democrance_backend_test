from rest_framework import serializers

from .models import Customer, Policy, PolicyHistory


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
        ]
        read_only_fields = ["id", "premium_amount", "policy_number", "end_date"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["customer"] = CustomerSerializer(instance.customer).data
        representation["has_expired"] = instance.has_expired
        return representation


class PolicyReadOnlySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    policy_number = serializers.CharField(read_only=True)
    policy_type = serializers.CharField(read_only=True)
    premium_amount = serializers.DecimalField(
        max_digits=9, decimal_places=2, read_only=True
    )


class PolicyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyHistory
        fields = ["policy", "status", "updated_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["policy"] = PolicyReadOnlySerializer(instance.policy).data

        return representation
