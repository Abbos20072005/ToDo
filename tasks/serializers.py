from random import choices
from wsgiref.util import request_uri

from rest_framework import serializers
from .models import Tasks, STATUS_CHOICES


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'author', "title", "description", "status", 'due_date', 'created_at']

class ParamsSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1, required=False)
    page_size = serializers.IntegerField(default=8, required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    due_date = serializers.DateField(required=False)
