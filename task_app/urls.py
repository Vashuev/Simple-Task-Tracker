from django.urls import path
from .views import TeamListCreateView, RegisterUser, TaskListCreateView, TaskUpdateView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('team/', TeamListCreateView.as_view(), name='team'),
    path('task/', TaskListCreateView.as_view(), name='task'),
    path('task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
]
