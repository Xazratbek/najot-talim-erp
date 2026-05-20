from django.urls import path

from .views import (
    StudentDashboardView,
    StudentGroupDetailView,
    StudentGroupsView,
    StudentIndicatorsDetailView,
    StudentIndicatorsView,
    StudentLessonDetailView,
    StudentPasswordChangeView,
    StudentPaymentsView,
    StudentRankingView,
    StudentSettingsView,
    StudentShopView,
)

urlpatterns = [
    path("", StudentDashboardView.as_view(), name="student-dashboard"),
    path("dashboard/", StudentDashboardView.as_view(), name="student-dashboard-alt"),
    path("payments/", StudentPaymentsView.as_view(), name="student-payments"),
    path("groups/", StudentGroupsView.as_view(), name="student-groups"),
    path("groups/<int:pk>/", StudentGroupDetailView.as_view(), name="student-group-detail"),
    path(
        "lessons/<int:pk>/",
        StudentLessonDetailView.as_view(),
        name="student-lesson-detail",
    ),
    path("indicators/", StudentIndicatorsView.as_view(), name="student-indicators"),
    path(
        "indicators/<str:reason>/",
        StudentIndicatorsDetailView.as_view(),
        name="student-indicators-detail",
    ),
    path("ranking/", StudentRankingView.as_view(), name="student-ranking"),
    path("shop/", StudentShopView.as_view(), name="student-shop"),
    path("settings/", StudentSettingsView.as_view(), name="student-settings"),
    path(
        "settings/password/",
        StudentPasswordChangeView.as_view(),
        name="student-password-change",
    ),
]
