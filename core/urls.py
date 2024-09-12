from django.urls import path

from .views import CustomerCreateApi, PolicyCreateApi

urlpatterns = [
    path("create_customer/", CustomerCreateApi.as_view(), name="customer-create"),
    path("quote/", PolicyCreateApi.as_view(), name="quote"),
]
