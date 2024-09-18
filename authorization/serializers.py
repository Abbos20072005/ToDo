from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=40, required=False)