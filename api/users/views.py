from rest_framework import viewsets
from api.users.models import User, UserRole
from api.users.serializers import UserSerializer, UserDetailSerializer, TeacherSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend

from asu_app.custom_permissions import ReadOnlyIfTeacher


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnlyIfTeacher]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group', 'role']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all().select_related('group')
        if self.request.user.role == UserRole.TEACHER:
            return (
                User.objects
                .filter(role=UserRole.STUDENT)
                .filter(
                    group__speciality__allowed_subjects__in=self.request.user.teacher_subjects.all()
                )
                .all().select_related('group').distinct()
            )


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response([], status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = UserDetailSerializer(data=request.data)
        user = authenticate(
            username=serializer.initial_data.get("username"),
            password=serializer.initial_data.get("password")
            )
        if not user:
            return Response(
                {'error': 'Invalid Credentials'},
                status=status.HTTP_404_NOT_FOUND
                )
        serializer = UserDetailSerializer(user)
        token, _ = Token.objects.get_or_create(user=user)
        json = {'token': token.key}
        json.update(serializer.data)

        return Response(json, status=status.HTTP_200_OK)


class TeacherCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, format='json'):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response([], status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
