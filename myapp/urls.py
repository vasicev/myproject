from django.urls import path, include
from .views import home, TagView, TaskView
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register('tag', TagView)
routers.register('task', TaskView)

urlpatterns = [
    path('task1/', home),
    path('task2-3/', include(routers.urls))
]