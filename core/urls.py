from django.urls import path

from .views import CustomerCreateApi, PolicyApi

urlpatterns = [
    path("create_customer/", CustomerCreateApi.as_view(), name="customer-create"),
    path("quote/", PolicyApi.as_view(), name="quote"),
    path("quote/<int:pk>/", PolicyApi.as_view(), name="quote-update"),
]
