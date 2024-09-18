from rest_framework.viewsets import ViewSet
from .models import Tasks
from .serializers import TaskSerializer, ParamsSerializer
from exceptions.exception import CustomApiException
from exceptions.error_message import ErrorCodes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .repository.get_task_page import get_page
from django.db.models import Q


class TasksCRUDViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: TaskSerializer},
        methods=['GET'],
        description="For getting the detail of one task, pk receive the id of task",
        tags=['Task']
    )
    def task_detail(self, request, pk):
        task = Tasks.objects.filter(id=pk, author_id=request.user.id).first()
        if not task:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND, message="Task not found")

        serializer = TaskSerializer(task, many=False)
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @extend_schema(
        request=TaskSerializer,
        responses={200: TaskSerializer},
        methods=['POST'],
        description="For create a task",
        tags=['Task']
    )
    def create_task(self, request):
        data = request.data
        data['author'] = request.user.id
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=TaskSerializer,
        responses={200: TaskSerializer},
        methods=['PATCH', 'PUT'],
        description="For update detail of one task, pk receive task id",
        tags=['Task']
    )
    def update_task(self, request, pk):
        task = Tasks.objects.filter(id=pk, author_id=request.user.id).first()
        if not task:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND, message='Task not found')

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @extend_schema(
        responses={204: "No content"},
        methods=['DELETE'],
        description="For delete the task, pk receive the task id",
        tags=['Task']
    )
    def delete_task(self, request, pk):
        task = Tasks.objects.filter(author_id=request.user.id, id=pk)
        if not task:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND, message='Task not found')

        task.delete()
        return Response(data={'result': "Task successfully deleted", 'ok': True}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        parameters=[
            OpenApiParameter(name='status', description="Filter by status", required=False, type=int),
            OpenApiParameter(name='due_date', type=OpenApiTypes.DATETIME, description="Filter by due_date"),
            OpenApiParameter(name='page', description='Page number', required=False, type=int),
            OpenApiParameter(name='page_size', description='Page size number', required=False, type=int)
        ],
        tags=['Task']
    )
    def tasks_filter(self, request):
        params_serializer = ParamsSerializer(data=request.query_params)
        if not params_serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=params_serializer.errors)

        due_date = params_serializer.validated_data.get('due_date')
        status = params_serializer.validated_data.get('status')
        page = params_serializer.validated_data.get('page')
        page_size = params_serializer.validated_data.get('page_size')

        filters = Q()
        if due_date:
            filters &= Q(due_date__lte=due_date)

        if status:
            filters &= Q(status=status)

        tasks = Tasks.objects.filter(filters, author_id=request.user.id)
        return Response(
            data={'result': get_page(context={'request': request, 'queryset': tasks}, page=page,
                                     page_size=page_size).data, 'ok': True})
