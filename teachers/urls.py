from django.urls import path
from .views import TeacherGroupDetailView, TeacherDashboardView

urlpatterns = [
    path('group_detail/<int:pk>/',TeacherGroupDetailView.as_view(),name='teacher_group_detail'),
    path('dashboard/',TeacherDashboardView.as_view(),name='teacher-dashboard')
]
