from django.urls import path

from .views import (
    TeacherCollectingGroupListView,
    TeacherDashboardView,
    TeacherGroupDetailView,
    TeacherGroupListView,
    TeacherProfileView,
)

urlpatterns = [
    path("dashboard/", TeacherDashboardView.as_view(), name="teacher-dashboard"),
    path("groups/", TeacherGroupListView.as_view(), name="teacher-groups"),
    path("collecting-groups/", TeacherCollectingGroupListView.as_view(), name="teacher-collecting-groups"),
    path("profile/", TeacherProfileView.as_view(), name="teacher-profile"),
    path("groups/<int:pk>/", TeacherGroupDetailView.as_view(), name="teacher_group_detail"),
]
