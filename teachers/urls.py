from django.urls import path

from .views import TeacherDetailUpdateDeleteAPI, TeacherListCreateAPI

urlpatterns = [
    path("", TeacherListCreateAPI.as_view(), name="teacher-list-create"),
    path("<int:pk>/", TeacherDetailUpdateDeleteAPI.as_view(), name="teacher-detail"),
]
