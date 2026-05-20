from django.urls import path

from .views import (
    TeacherAttendanceView,
    TeacherCollectingGroupListView,
    TeacherDashboardView,
    TeacherGroupDetailView,
    TeacherLessonDetailView,
    TeacherGroupListView,
    TeacherHomeworkCreateView,
    TeacherProfileView,
)

urlpatterns = [
    path("dashboard/", TeacherDashboardView.as_view(), name="teacher-dashboard"),
    path("groups/", TeacherGroupListView.as_view(), name="teacher-groups"),
    path("collecting-groups/", TeacherCollectingGroupListView.as_view(), name="teacher-collecting-groups"),
    path("profile/", TeacherProfileView.as_view(), name="teacher-profile"),
    path("groups/<int:pk>/", TeacherGroupDetailView.as_view(), name="teacher_group_detail"),
    path("groups/<int:pk>/homeworks/new/", TeacherHomeworkCreateView.as_view(), name="teacher-homework-create"),
    path("groups/<int:pk>/lessons/<int:lesson_id>/", TeacherLessonDetailView.as_view(), name="teacher-lesson-detail"),
    path("groups/<int:pk>/attendance/", TeacherAttendanceView.as_view(), name="teacher-attendance"),
]
