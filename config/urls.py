from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('task_manager.urls')),
    path('accounts/', include('allauth.urls')),
    path('ai_support/', include('ai_support.urls')),
    path('learning/', include('learning.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
