from django.urls import path

from .views import CustomerCreateApi, PolicyApi, PolicyHistoryApi

urlpatterns = [
    path("create_customer/", CustomerCreateApi.as_view(), name="customer-create"),
    path("quote/", PolicyApi.as_view(), name="quote"),
    path("quote/<int:pk>/", PolicyApi.as_view(), name="quote-update"),
    path("policies/", PolicyApi.as_view(), name="policy-list"),
    path("policies/<int:pk>/", PolicyApi.as_view(), name="policy-details"),
    path(
        "policies/<int:pk>/history/", PolicyHistoryApi.as_view(), name="policy-history"
    ),
]
