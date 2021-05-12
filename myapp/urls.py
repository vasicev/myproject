from django.urls import path, include
from .views import first_task, home, TagList, TaskList
from rest_framework import routers
import oauth2_provider.views as oauth2_views

#routers = routers.DefaultRouter()
#routers.register('tag', TagList.as_view())
#routers.register('task', TaskList.as_view())

urlpatterns = [
    path('', home),
    path('first_task/', first_task, name='first_task'),
    #path('api/', include(routers.urls), name='api'),
    path('tags/', TagList.as_view(), name='tags'),
    path('tasks/', TaskList.as_view(), name='tasks')
    #path('authorized_api/', authorized_api)
]