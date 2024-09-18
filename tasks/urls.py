from django.urls import path
from .views import TasksCRUDViewSet


urlpatterns = [
    path('<int:pk>/', TasksCRUDViewSet.as_view({'get': "task_detail", 'patch': 'update_task', 'delete': "delete_task"})),
    path('create/', TasksCRUDViewSet.as_view({'post': "create_task"})),
    path('filter/', TasksCRUDViewSet.as_view({'get': 'tasks_filter'}))
]