from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View

from exams.models import Exam
from attendance.models import Attendance, Status
from groups.models import Group, GroupLesson
from homeworks.models import HomeWorkStatusChoices, Homework, HomeworkSubmission
from notifications.models import Notification, NotificationTypes
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
        if request.POST.get("action") == "create_homework":
            group_lesson = get_object_or_404(GroupLesson, pk=request.POST.get("lesson_id"), group=group)
            description = request.POST.get("description", "").strip()
            deadline = request.POST.get("deadline")
            if description and deadline:
                homework, _ = Homework.objects.update_or_create(
                    group_lesson=group_lesson,
                    defaults={"description": description, "deadline": deadline},
                )
                for gs in group.students.select_related("student"):
                    Notification.objects.create(
                        receiver=gs.student,
                        type=NotificationTypes.NEW_LESSON,
                        title=f"{group.name}: {group_lesson.lesson.title} darsiga uyga vazifa qo'shildi",
                    )
                messages.success(request, "Uyga vazifa saqlandi.")
            else:
                messages.error(request, "Tavsif va deadline majburiy.")
        return redirect(f"{request.path}?tab=materials&material_tab=lessons")

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
        lesson_rows = []
        for lesson in lessons:
            homework = Homework.objects.filter(group_lesson=lesson).first()
            stats = {"submitted": 0, "waiting": 0, "approved": 0}
            if homework:
                stats = HomeworkSubmission.objects.filter(homework=homework).aggregate(
                    submitted=Count("id", filter=~Q(status=HomeWorkStatusChoices.NOT_SUBMITTED)),
                    waiting=Count("id", filter=Q(status=HomeWorkStatusChoices.WAITING)),
                    approved=Count("id", filter=Q(status=HomeWorkStatusChoices.APPROVED)),
                )
            lesson_rows.append({"lesson": lesson, "homework": homework, "stats": stats})

        exams = Exam.objects.filter(group=group).order_by("-started_at")

        return render(
            request,
            self.template_name,
            {
                "guruh": group,
                "tab": tab,
                "material_tab": material_tab,
                "lessons": lessons,
                "lesson_rows": lesson_rows,
                "exams": exams,
            },
        )


class TeacherLessonDetailView(TeacherRequiredMixin, View):
    template_name = "teachers/teacher_lesson_detail.html"

    def post(self, request, pk, lesson_id):
        group = get_object_or_404(Group.objects.filter(teachers__teacher=request.user), pk=pk)
        if request.POST.get("action") == "review_submission":
            sub = get_object_or_404(HomeworkSubmission, pk=request.POST.get("submission_id"), homework__group_lesson_id=lesson_id, homework__group_lesson__group=group)
            sub.status = request.POST.get("status", HomeWorkStatusChoices.WAITING)
            sub.teacher_comment = request.POST.get("teacher_comment", "")
            sub.checked_by = request.user
            sub.checked_at = timezone.now()
            sub.allow_resubmission = request.POST.get("allow_resubmission") == "on"
            sub.save()
            Notification.objects.create(receiver=sub.student, type=NotificationTypes.HOMEWORK_REVIEWED, title=f"{group.name}: {sub.homework.group_lesson.lesson.title} vazifangiz tekshirildi")
        return redirect("teacher-lesson-detail", pk=pk, lesson_id=lesson_id)

    def get(self, request, pk, lesson_id):
        group = get_object_or_404(Group.objects.filter(teachers__teacher=request.user), pk=pk)
        lesson = get_object_or_404(GroupLesson.objects.select_related("lesson"), pk=lesson_id, group=group)
        homework = Homework.objects.filter(group_lesson=lesson).first()
        submissions = HomeworkSubmission.objects.filter(homework=homework).select_related("student") if homework else []
        return render(request, self.template_name, {"guruh": group, "lesson": lesson, "homework": homework, "submissions": submissions})


class TeacherAttendanceView(TeacherRequiredMixin, View):
    template_name = "teachers/teacher_attendance.html"

    def get_group(self, request, pk):
        return get_object_or_404(Group.objects.filter(teachers__teacher=request.user).prefetch_related("students__student"), pk=pk)

    def post(self, request, pk):
        group = self.get_group(request, pk)
        lesson = get_object_or_404(GroupLesson, pk=request.POST.get("lesson_id"), group=group)
        for gs in group.students.select_related("student"):
            val = request.POST.get(f"student_{gs.student_id}", Status.ABSENT)
            Attendance.objects.update_or_create(group_lesson=lesson, student=gs.student, defaults={"status": val})
        messages.success(request, "Yo'qlama saqlandi")
        return redirect("teacher-attendance", pk=pk)

    def get(self, request, pk):
        group = self.get_group(request, pk)
        lessons = GroupLesson.objects.filter(group=group).select_related("lesson").order_by("-lesson__lesson_date")
        selected = lessons.first()
        return render(request, self.template_name, {"guruh": group, "lessons": lessons, "selected": selected})
