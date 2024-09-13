from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Policy, PolicyHistory
from .serializers import CustomerSerializer, PolicyHistorySerializer, PolicySerializer


class CustomerCreateApi(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomerSerializer

    # filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    # search_fields = ['first_name', 'last_name', 'email']
    # filterset_fields = ['date_of_birth']

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        queryset = Customer.objects.all()

        first_name = request.query_params.get("first_name", None)
        last_name = self.request.query_params.get("last_name", None)
        email = self.request.query_params.get("email", None)
        date_of_birth = self.request.query_params.get("date_of_birth", None)

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


class PolicyApi(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PolicySerializer

    def post(self, request):
        serializer = PolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            policy = get_object_or_404(Policy, id=pk)
            serializer = PolicySerializer(policy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            customer_id = request.query_params.get("customer_id", None)
            if customer_id:
                policies = Policy.objects.filter(
                    customer_id=customer_id
                ).select_related("customer")
            else:
                policies = Policy.objects.select_related("customer")

            serializer = PolicySerializer(policies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        policy = get_object_or_404(Policy, id=pk)
        serializer = PolicySerializer(policy, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolicyHistoryApi(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PolicyHistorySerializer

    def get(self, request, pk=None, *args, **kwargs):
        policy = get_object_or_404(Policy, id=pk)
        history = PolicyHistory.objects.filter(policy=policy).select_related("policy")
        serializer = PolicyHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
