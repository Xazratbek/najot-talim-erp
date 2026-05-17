from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/',include('users.urls')),
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
