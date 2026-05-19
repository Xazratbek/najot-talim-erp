from users.utils import generate_login_code
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.models import User
from users.forms import AdminStudentCreateForm
from django.urls import reverse_lazy


class AdminStudentCreateView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    model = User
    form_class = AdminStudentCreateForm
    template_name = 'accounts/student_create.html'
    success_url = reverse_lazy('student_list')

    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)

    def form_valid(self, form):
        user = form.save(commit=False)
        username = generate_login_code()
        while User.objects.filter(username=username).exists():
            username = generate_login_code()
        user.username = username

        generated_password = User.objects.make_random_password(length=6)
        user.set_password(generated_password)
        user.save()
        return super().form_valid(form)