from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.models import Roles
from groups.models import GroupTeacher, Group, GroupLesson, GroupStudent
from lessons.forms import LessonForm
from notifications.models import Notification,NotificationTypes



class TeacherRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == Roles.TEACHER
        )
    

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

        teacher_groups = request.user.group_teachers.all() 

        for gr in teacher_groups:
            teacher_group = GroupTeacher.objects.filter(group = gr, teacher = request.user)



        group = Group.objects.prefetch_related("teachers", "students", "group_lessons").filter(pk = pk, teacher = request.user)
        if group:
            context = {
                "group":group,
                "group_teachers":group.teachers.all(),
                "group_students":group.students.all(), 
                "group_lessons":group.group_lessons.all()
            }
            return render(request, "teachers/teacher_group_detail.html", context=context)


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