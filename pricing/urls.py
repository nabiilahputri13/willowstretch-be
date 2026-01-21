from django.urls import path

from .views import BuyPackageAPI, MySubscriptionListAPI, PackageDetailAPI, PackageListCreateAPI

urlpatterns = [
    # Admin & Public: Manajemen Paket
    path("", PackageListCreateAPI.as_view(), name="package-list"),
    path("<int:pk>/", PackageDetailAPI.as_view(), name="package-detail"),
    # User Transaction
    path("buy/<int:package_id>/", BuyPackageAPI.as_view(), name="buy-package"),
    path("my-subscriptions/", MySubscriptionListAPI.as_view(), name="my-subs"),
]
