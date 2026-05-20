from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from exams.models import Exam
from groups.models import Group, GroupLesson
from homeworks.models import HomeWorkStatusChoices, Homework, HomeworkSubmission
from users.models import Roles


class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role in [Roles.TEACHER, Roles.SUPPORT_TEACHER]


class TeacherDashboardView(TeacherRequiredMixin, View):
    def get(self, request):
        return redirect("teacher-groups")


class TeacherGroupListView(TeacherRequiredMixin, View):
    template_name = "teachers/teacher_groups.html"

    def get(self, request):
        groups = (
            Group.objects.filter(teachers__teacher=request.user, is_opened=True)
            .select_related("course", "branch")
            .prefetch_related("teachers__teacher")
            .distinct()
        )
        return render(request, self.template_name, {"groups": groups})


class TeacherCollectingGroupListView(TeacherRequiredMixin, View):
    template_name = "teachers/collecting_groups.html"

    def get(self, request):
        groups = (
            Group.objects.filter(teachers__teacher=request.user, is_opened=False)
            .select_related("course", "branch")
            .prefetch_related("teachers__teacher")
            .distinct()
        )
        return render(request, self.template_name, {"groups": groups})


class TeacherProfileView(TeacherRequiredMixin, View):
    def get(self, request):
        return render(request, "teachers/profile.html")


class TeacherGroupDetailView(TeacherRequiredMixin, View):
    template_name = "teachers/teacher_group_detail.html"

    def get_group(self, request, pk):
        return get_object_or_404(
            Group.objects.filter(teachers__teacher=request.user)
            .select_related("course", "branch")
            .prefetch_related("teachers__teacher", "students__student"),
            pk=pk,
        )

    def post(self, request, pk):
        group = self.get_group(request, pk)
        if request.POST.get("action") == "review_submission":
            sub = get_object_or_404(
                HomeworkSubmission,
                pk=request.POST.get("submission_id"),
                homework__group_lesson__group=group,
            )
            sub.status = request.POST.get("status", HomeWorkStatusChoices.WAITING)
            sub.teacher_comment = request.POST.get("teacher_comment", "")
            sub.checked_by = request.user
            sub.checked_at = timezone.now()
            sub.allow_resubmission = request.POST.get("allow_resubmission") == "on"
            sub.save()
        return redirect(f"{request.path}?tab=materials&material_tab=lessons&lesson={request.POST.get('lesson_id', '')}")

    def get(self, request, pk):
        group = self.get_group(request, pk)
        tab = request.GET.get("tab", "info")
        material_tab = request.GET.get("material_tab", "lessons")

        lessons = (
            GroupLesson.objects.filter(group=group)
            .select_related("lesson")
            .prefetch_related("homeworks__submissions__student")
            .order_by("-lesson__lesson_date")
        )
        selected_lesson = None
        lesson_id = request.GET.get("lesson")
        if lesson_id:
            selected_lesson = lessons.filter(pk=lesson_id).first()
        if not selected_lesson and lessons:
            selected_lesson = lessons.first()

        lesson_homework = Homework.objects.filter(group_lesson=selected_lesson).first() if selected_lesson else None
        submissions = []
        submission_stats = {"topshirgan": 0, "topshirmagan": 0, "tekshirilmagan": 0}
        if lesson_homework:
            submissions = list(
                HomeworkSubmission.objects.filter(homework=lesson_homework)
                .select_related("student", "checked_by")
                .order_by("student__first_name", "student__last_name")
            )
            agg = HomeworkSubmission.objects.filter(homework=lesson_homework).aggregate(
                topshirgan=Count("id", filter=~Q(status=HomeWorkStatusChoices.NOT_SUBMITTED)),
                topshirmagan=Count("id", filter=Q(status=HomeWorkStatusChoices.NOT_SUBMITTED)),
                tekshirilmagan=Count("id", filter=Q(checked_at__isnull=True) & ~Q(status=HomeWorkStatusChoices.NOT_SUBMITTED)),
            )
            submission_stats = {k: (v or 0) for k, v in agg.items()}

        exams = Exam.objects.filter(group=group).order_by("-started_at")

        return render(
            request,
            self.template_name,
            {
                "guruh": group,
                "tab": tab,
                "material_tab": material_tab,
                "lessons": lessons,
                "selected_lesson": selected_lesson,
                "lesson_homework": lesson_homework,
                "submissions": submissions,
                "submission_stats": submission_stats,
                "exams": exams,
            },
        )
