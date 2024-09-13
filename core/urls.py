from django.urls import path

from .views import (
    CustomerCreateApi,
    CustomerListApi,
    PolicyCreateApi,
    PolicyDetailApi,
    PolicyHistoryListApi,
    PolicyListApi,
)

urlpatterns = [
    path("create-customer/", CustomerCreateApi.as_view(), name="customer-create"),
    path("customers/", CustomerListApi.as_view(), name="customer-list"),
    path("quote/", PolicyCreateApi.as_view(), name="quote-create"),
    path("quote/<int:pk>/", PolicyDetailApi.as_view(), name="quote-detail"),
    path("policies/", PolicyListApi.as_view(), name="policy-list"),
    path("policies/<int:pk>/", PolicyDetailApi.as_view(), name="policy-detail"),
    path(
        "policies/<int:pk>/history/",
        PolicyHistoryListApi.as_view(),
        name="policy-history",
    ),
]
