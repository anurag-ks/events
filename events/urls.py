from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('', include('main.urls')),
]
