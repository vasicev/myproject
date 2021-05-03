from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Tag, Task, TagSerializer, TaskSerializer

def home(request):
    return HttpResponse('Hello Wolrd!')

class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
