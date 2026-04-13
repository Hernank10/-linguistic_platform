from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('courses/', include('apps.courses.urls')),
    path('exercises/', include('apps.exercises.urls')),
    path('flashcards/', include('apps.flashcards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
