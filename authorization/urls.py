from django.urls import path
from .views import AuthViewSet

urlpatterns = [
    path('register/', AuthViewSet.as_view({'post': "user_register"})),
    path('login/', AuthViewSet.as_view({'post': "user_login"}))
]