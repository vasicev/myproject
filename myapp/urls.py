from django.urls import path
from .views import home

urlpatterns = [
    path('task1/', home)
]