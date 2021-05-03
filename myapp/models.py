from django.db import models
from rest_framework import serializers

class Tag(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tag = models.ManyToManyField(Tag)
    def __str__(self):
        return self.title

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
