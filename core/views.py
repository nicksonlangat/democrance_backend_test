from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Policy, PolicyHistory
from .serializers import CustomerSerializer, PolicyHistorySerializer, PolicySerializer


class CustomerCreateApi(APIView):
    """
    View to create new customers.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerSerializer

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerListApi(APIView):
    """
    View to list all customers and filter them.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerSerializer

    def get(self, request, *args, **kwargs):
        queryset = Customer.objects.all()

        first_name = request.query_params.get("first_name", None)
        last_name = request.query_params.get("last_name", None)
        email = request.query_params.get("email", None)
        date_of_birth = request.query_params.get("date_of_birth", None)

        if first_name:
            queryset = queryset.filter(first_name__iexact=first_name)

        if last_name:
            queryset = queryset.filter(last_name__iexact=last_name)

        if email:
            queryset = queryset.filter(email__iexact=email)

        if date_of_birth:
            queryset = queryset.filter(date_of_birth__iexact=date_of_birth)

        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PolicyCreateApi(APIView):
    """
    View to create new policies/quotes.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PolicySerializer

    def post(self, request):
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyListApi(APIView):
    """
    View to list all policies and filter them.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PolicySerializer

    def get(self, request, *args, **kwargs):
        policies = Policy.objects.select_related("customer")

        customer_id = request.query_params.get("customer_id", None)
        policy_type = request.query_params.get("policy_type", None)
        policy_status = request.query_params.get("policy_status", None)

        if customer_id:
            policies = policies.filter(customer_id=customer_id)

        if policy_status:
            policies = policies.filter(policy_status__iexact=policy_status)

        if policy_type:
            policies = policies.filter(policy_type__iexact=policy_type)

        serializer = PolicySerializer(policies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PolicyDetailApi(APIView):
    """
    View to view a single policy or update it.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PolicySerializer

    def get(self, request, pk=None, *args, **kwargs):
        policy = get_object_or_404(Policy, id=pk)
        serializer = PolicySerializer(policy)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        policy = get_object_or_404(Policy, id=pk)
        serializer = PolicySerializer(policy, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyHistoryListApi(APIView):
    """
    View to track status changes of a given policy.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = PolicyHistorySerializer

    def get(self, request, pk=None, *args, **kwargs):
        policy = get_object_or_404(Policy, id=pk)
        history = PolicyHistory.objects.filter(policy=policy).select_related("policy")
        serializer = PolicyHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
