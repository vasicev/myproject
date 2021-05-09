from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response as RestResponse
from rest_framework.decorators import action, renderer_classes, api_view, permission_classes, authentication_classes
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Tag, Task, TagSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from oauth2_provider.models import Application, Grant, RefreshToken, AccessToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
import requests
import json
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from django.contrib.auth.models import User, Group

def first_task(request):
    return HttpResponse('Hello World!')


def home(request):
    return render(request, 'home.html')

def curl(type, url, headers=None, data=None):
    if 'get'.__eq__(type):
        req = requests.get(url, headers=headers, data=data)
        print('\n\n' + str(req.json()) + '\n\n')
        return req
    elif 'post'.__eq__(type):
        req = requests.post(url, headers=headers, data=json.dumps(data))
        print('\n\n' + str(req.json()) + '\n\n')
        return req
    elif 'put'.__eq__(type):
        req = requests.put(url, headers=headers, data=json.dumps(data))
        print('\n\n' + str(req.json()) + '\n\n')
        return req

@api_view(('GET',))
# @renderer_classes((JSONRenderer, TemplateHTMLRenderer))
@permission_classes((AllowAny,))
# @authentication_classes(OAuth2Authentication)
def authorized_api(request):
    myapp = Application.objects.get(name='myapp')
    client_id = myapp.client_id
    client_secret = myapp.client_secret
    url = 'http://127.0.0.1:8000/o/token/'
    access_token = AccessToken.objects.last()
    if access_token:
        model = str(request.GET.get('m', ''))
        url = 'http://127.0.0.1:8000/api/'
        if model:
            url += model
        headers = {
            'Authorization': f"Bearer {access_token}"
        }
        option = str(request.GET.get('op', ''))
        if 'tag'.__eq__(model):
            title = str(request.GET.get('title', ''))
            if 'post'.__eq__(option) and title:
                url += '/'
                headers['Content-Type'] = 'application/json'
                data = {
                    'title': title
                }
                req = curl('post', url, headers, data)
            elif 'put'.__eq__(option) and title:
                pk = str(request.GET.get('pk', ''))
                url += '/' + pk + '/'
                print('url: --> ' + url + ' option=' + option)
                headers['Content-Type'] = 'application/json'
                data = {
                    'title': title
                }
                req = curl('put', url, headers, data)
            else:
                req = curl('get', url, headers)
        else:
            # print('url: --> ' + url + ' option=' + option)
            req = curl('get', url, headers)
        valid = req.status_code != 401
    if access_token and not valid:
        access_token.delete()
    if access_token and valid:
        res = json.loads(req.text)
        if not model:
            res['tag'] = 'http://127.0.0.1:8000/authorized_api/?m=tag'
            res['task'] = 'http://127.0.0.1:8000/authorized_api/?m=task'
        return RestResponse(res)
    else:
        refresh_token = RefreshToken.objects.last()
        if refresh_token:
            data = {
                'grant_type': 'refresh_token',
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token
            }
            req = requests.post(url, data=data)
            valid = req.status_code != 401
        if refresh_token and not valid:
            refresh_token.delete()
        if refresh_token and valid:
            res = json.loads(req.text)
            return HttpResponse(f"<p style=\"font-family:monospace\">{res}<p>")
        else:
            code = Grant.objects.last()
            if code:
                headers = {
                    'Cache-Control': 'no-cache',
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                data = {
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': code,
                    'redirect_uri': 'http://127.0.0.1:8000/',
                    'grant_type': 'authorization_code'
                }
                req = requests.post(url, headers=headers, data=data)
                valid = req.status_code != 401
            if code and not valid:
                code.delete()
            if code and valid:
                res = json.loads(req.text)
                return HttpResponse(f"<p style=\"font-family:monospace\">{res}<p>")
            else:
                return redirect(
                    'http://127.0.0.1:8000/o/authorize/' +
                    '?response_type=code' +
                    f'&client_id={client_id}'
                    '&redirect_uri=http://127.0.0.1:8000/'
                )

class TagView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    # authentication_classes = [OAuth2Authentication]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
        

class TaskView(viewsets.ModelViewSet):
    #permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        query_params = self.request.query_params
        params = dict(query_params)
        if params:
            filtered_tags = Tag.objects.filter(title__in=params['title'])
            print("PRINT = " + str(filtered_tags))
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
