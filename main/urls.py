from django.urls import path, include
from .views import index, get_permalink, create_event

urlpatterns = [
    path('', index, name='index'),
    path('accounts/logout/', include('django.contrib.auth.urls')),
    path('get_permalink/', get_permalink, name='get_permalink'),
    path('<str:username>/<int:id>', create_event, name='create_event')
]
