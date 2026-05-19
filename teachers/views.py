from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.models import Roles
from groups.models import GroupTeacher
from lessons.forms import LessonForm
from notifications.models import Notification,NotificationTypes

class TeacherCollectingGroupListView(LoginRequiredMixin,UserPassesTestMixin,View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == Roles.TEACHER

    def get(self, request):
        teacher = request.user
        groups = GroupTeacher.objects.filter(teacher=teacher,group__is_opened=False).select_related('group')

        return render(request,'teacher/collecting_groups.html',context={"groups":groups})

### View: `TeacherLessonCreateView`
# **Mas'ul:** Xazratbek
# **Vazifa:** Yangi lesson yaratish.

# **Logika:**
# 1. Teacher groupga tegishli ekanligi tekshiriladi.
# 2. Lesson sanasi, mavzu, material validatsiya.
# 3. Lesson yaratilgach guruh studentlariga notification queue qilinadi.

class TeacherLessonCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == Roles.TEACHER

    def get(self, request):
        form = LessonForm()
        return render(request,"teacher/lesson_create.html",context={'form':form})

    def post(self, request):
        form = LessonForm(data=request.POST)
        if form.is_valid():
            form.save()
            Notification.objects.create(receiver=request.user,type=NotificationTypes.NEW_LESSON,title="Yangi dars boshlandi")
            return render(request,)