from django.urls import path

from .views import (
    CancelClassAPI,
    JoinClassAPI,
    MyJoinedClassesAPI,
    YogaClassDetailUpdateDeleteAPI,
    YogaClassListCreateAPI,
)

urlpatterns = [
    path("", YogaClassListCreateAPI.as_view(), name="class-list-create"),
    path("<int:pk>/", YogaClassDetailUpdateDeleteAPI.as_view(), name="class-detail"),
    path("<int:pk>/join/", JoinClassAPI.as_view(), name="class-join"),
    path("<int:pk>/cancel/", CancelClassAPI.as_view(), name="class-cancel"),
    path("me/", MyJoinedClassesAPI.as_view(), name="my-classes"),
]
