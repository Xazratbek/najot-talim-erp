from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('users.urls')),
    path('attendances/',include('attendance.urls')),
    path('branches/',include('branches.urls')),
    path('courses/',include('courses.urls')),
    path('groups/',include('groups.urls')),
    path('gamifications/',include('gamification.urls')),
    path('homeworks/',include('homeworks.urls')),
    path('lessons/',include('lessons.urls')),
    path('exams/',include('exams.urls')),
    path('payments/',include('payments.urls')),
    path('shops/',include('shop.urls')),
    path('student/',include('students.urls')),
    path('teacher/',include('teachers.urls')),
]

if settings.DEBUG:
    if not str(settings.STATIC_URL).startswith('http'):
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if getattr(settings, 'MEDIA_ROOT', None):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()