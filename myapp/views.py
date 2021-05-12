from django.shortcuts import render, redirect
from django.http import HttpResponse
from oauth2_provider.contrib.rest_framework.permissions import TokenHasResourceScope
from rest_framework import viewsets
from rest_framework.response import Response as RestResponse
from rest_framework.decorators import action, renderer_classes, api_view, permission_classes, authentication_classes
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Tag, Task, TagSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView
from oauth2_provider.models import Application, Grant, RefreshToken, AccessToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
import requests
import json

from django.contrib.auth.models import User, Group

def first_task(request):
    return HttpResponse('Hello World!')


def home(request):
    return render(request, 'home.html')


class TagList(ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
        

class TaskList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
