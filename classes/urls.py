from django.urls import path
from .views import YogaClassListCreateAPI, YogaClassDetailUpdateDeleteAPI

urlpatterns = [
    path('', YogaClassListCreateAPI.as_view(), name='class-list-create'),
    path('<int:pk>/', YogaClassDetailUpdateDeleteAPI.as_view(), name='class-detail'),
]