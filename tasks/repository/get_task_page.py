from rest_framework.pagination import PageNumberPagination
from ..serializers import TaskSerializer

def get_page(context: dict, page: int, page_size: int):
    queryset = context.get('queryset')
    request = context.get('request')
    pagination = PageNumberPagination()
    pagination.page = page
    pagination.page_size = page_size
    paginated = pagination.paginate_queryset(queryset, request)
    serializer = TaskSerializer(paginated, many=True).data

    return pagination.get_paginated_response(data=serializer)