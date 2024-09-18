from datetime import datetime
from rest_framework import serializers

from exceptions.error_message import ErrorCodes
from exceptions.exception import CustomApiException
from .models import Tasks, STATUS_CHOICES


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'author', "title", "description", "status", 'due_date', 'created_at']
        read_only_fields = ('author',)

    def validate(self, attrs):
        if attrs.get('due_date') and attrs.get('due_date') < datetime.now().date():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message="Due date could not be less then now date")
        return attrs


class ParamsSerializer(serializers.Serializer):
    page = serializers.IntegerField(default=1, required=False)
    page_size = serializers.IntegerField(default=8, required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False)
    due_date = serializers.DateField(required=False)
