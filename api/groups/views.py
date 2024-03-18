from rest_framework import viewsets
from api.groups.models import Group, Speciality
from api.groups.serializers import GroupSerializer, SpecialitySerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from asu_app.custom_permissions import ReadOnly
from api.users.models import UserRole


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser | ReadOnly]
    queryset = Group.objects.all().select_related('speciality').distinct()
    serializer_class = GroupSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_anonymous:
            return Group.objects.all().select_related('speciality').distinct()
        if self.request.user.role == UserRole.TEACHER:
            return (
                Group.objects
                .filter(speciality__allowed_subjects__in=self.request.user.teacher_subjects.all())
                .all().select_related('speciality').distinct()
            )


class SpecialityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer
