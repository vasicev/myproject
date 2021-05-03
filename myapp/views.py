from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response as RestResponse
from rest_framework.decorators import action
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Tag, Task, TagSerializer, TaskSerializer

def home(request):
    return HttpResponse('Hello Wolrd!')

class TagView(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
        

class TaskView(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        query_params = self.request.query_params
        params = dict(query_params)
        if params:
            filtered_tags = Tag.objects.filter(title__in=params['title'])
            tagIDs = []
            for tag in filtered_tags:
                tagIDs.append(tag.pk)
            filtered_task = Task.objects.filter(tag__in=tagIDs).distinct()
            if filtered_task:
                serializer = TaskSerializer(filtered_task, many=True)
                return RestResponse(serializer.data)
            else:
                return RestResponse({'detail': 'Not found'}, status=HTTP_404_NOT_FOUND)
        else:
            serializer = TaskSerializer(self.queryset, many=True)
            return RestResponse(serializer.data)

    @action(detail=False)
    def filter(self, request):
        query_params = self.request.query_params
        params = dict(query_params)
        if params:
            filtered_tags = Tag.objects.filter(title__in=params['title'])
            tagIDs = []
            for tag in filtered_tags:
                tagIDs.append(tag.pk)
            filtered_task = Task.objects.filter(tag__in=tagIDs).distinct()
            if filtered_task:
                serializer = TaskSerializer(filtered_task, many=True)
                return RestResponse(serializer.data)
            else:
                return RestResponse({'detail': 'Not found'}, status=HTTP_404_NOT_FOUND)
        else:
            return RestResponse({'e.g1' : 'filter/?title=<title>', 'e.g2' : 'filter/?title=<title>&title=<title2>'})
