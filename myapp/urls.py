from django.urls import path, include
from .views import TagView, TaskView, first_task, home, authorized_api
from rest_framework import routers
import oauth2_provider.views as oauth2_views

routers = routers.DefaultRouter()
routers.register('tag', TagView)
routers.register('task', TaskView)

urlpatterns = [
    path('', home),
    path('first_task/', first_task),
    path('api/', include(routers.urls)),
    path('authorized_api/', authorized_api)
]