from rest_framework import routers
from api.users.views import UserViewSet
from django.urls import path, include
from api.users.views import RegisterUser, LoginView, TeacherCreateView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUser.as_view(), name='register'),
    path('token-auth/', LoginView.as_view(), name='token-auth'),
    path('create-teacher/', TeacherCreateView.as_view(), name='create-teacher')
]
