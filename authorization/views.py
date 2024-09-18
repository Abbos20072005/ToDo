from datetime import datetime
from rest_framework.viewsets import ViewSet

from .models import User
from exceptions.exception import CustomApiException
from exceptions.error_message import ErrorCodes
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import login_validation
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema


class AuthViewSet(ViewSet):
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        description="For create user",
        methods=["POST"],
        tags=['Authorization']
    )
    def user_register(self, request):
        user = User.objects.filter(username=request.data.get('username')).first()
        if user:
            raise CustomApiException(error_code=ErrorCodes.USER_ALREADY_EXIST)

        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=UserLoginSerializer,
        responses={200: UserLoginSerializer},
        description="For login user",
        methods=['POST'],
        tags=['Authorization']
    )
    def user_login(self, request):
        login_serializer = UserLoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=login_serializer.errors)

        login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        user = login_validation(request.data)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        access_token['login_time'] = login_time

        user.last_login = login_time
        user.save()
        return Response({'result': {'access_token': str(access_token), "refresh_token": str(refresh)}, 'ok': True},
                        status=status.HTTP_200_OK)
