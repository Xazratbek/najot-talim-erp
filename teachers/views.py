from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.models import Roles
from groups.models import GroupTeacher, Group, GroupLesson, GroupStudent
from lessons.forms import LessonForm
from notifications.models import Notification,NotificationTypes
from django.db.models import Prefetch, Q
from users.models import User

class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == Roles.TEACHER or self.request.user.role == Roles.SUPPORT_TEACHER
        )

class TeacherDashboardView(TeacherRequiredMixin,View):
    def get(self, request):
        groups = GroupTeacher.objects.filter(teacher=request.user)
        return render(request,'teachers/teacher_dashboard.html',context={'groups':groups})

class TeacherCollectingGroupListView(TeacherRequiredMixin, View):
    def get(self, request):
        teacher = request.user
        groups = GroupTeacher.objects.filter(teacher=teacher,group__is_opened=False).select_related('group')

        return render(request,'teachers/collecting_groups.html',context={"groups":groups})

class TeacherGroupListView(TeacherRequiredMixin, View):
    def get(self, request):
        teacher = request.user
        groups = GroupTeacher.objects.filter(teacher=teacher,group__is_opened=True).select_related('group')

        return render(request,'teachers/teacher_groups.html',context={"groups":groups})

class TeacherGroupDetailView(TeacherRequiredMixin, View):
    def get(self, request, pk):
        guruh = GroupTeacher.objects.filter(teacher=request.user,group__id=pk).first().group
        students = []
        for student in guruh.students.select_related('student'):
            students.append(student.student)

        guruh_darslari_vazifalari = []
        guruh_uyga_vazifalari = []
        for dars in guruh.group_lessons.all():
            for homework in dars.homeworks.all():
                data = {
                    "dars":dars.lesson.title,
                    'dars_sanasi': dars.lesson.lesson_date,
                    "deadline":homework.deadline,
                    "uyga_vazifa_berilgan_sana": homework.created_at,
                    "homework":homework,
                }
                guruh_uyga_vazifalari.append(data)

        return render(request,'teachers/teacher_group_detail.html',context={"guruh":guruh,"students":students,"guruh_darslari":guruh_darslari_vazifalari,"guruh_uyga_vazifalari":guruh_uyga_vazifalari})

class TeacherLessonCreateView(TeacherRequiredMixin, View):
    def get(self, request):
            pass

class TeacherLessonCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == Roles.TEACHER

    def get(self, request):
        form = LessonForm()
        return render(request,"teachers/lesson_create.html",context={'form':form})

    def post(self, request):
        form = LessonForm(data=request.POST)
        if form.is_valid():
            lesson = form.save()
            notifications = []
            for student in lesson.lesson_group.group.students.all():
                notifications.append(Notification(receiver=student.student,type=NotificationTypes.NEW_LESSON,title=f"{student.student.get_full_name()}-Yangi dars boshlandi"))
            Notification.objects.bulk_create(notifications)
            return redirect('teacher-groups')