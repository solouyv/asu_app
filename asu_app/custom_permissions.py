from rest_framework.permissions import BasePermission, SAFE_METHODS
from asu_app.settings import SYSTEM_ADMINISTRATION_SUBJECT_ID
from api.subjects.models import Subject
from api.users.models import UserRole


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ReadOnlyIfAllowed(BasePermission):

    def has_permission(self, request, view):
        sys_adm_subj = Subject.objects.prefetch_related('allowed_specialities').get(
            pk=SYSTEM_ADMINISTRATION_SUBJECT_ID
        )

        if request.user.role == UserRole.STUDENT:
            if (
                request.method in SAFE_METHODS
                and request.user.group.speciality
                in sys_adm_subj.allowed_specialities.all()
            ):
                return True
            return False
        else:
            if (
                request.method in SAFE_METHODS
                and sys_adm_subj in request.user.teacher_subjects.all()
            ):
                return True
            return False


class ConsolePermissions(BasePermission):

    def has_permission(self, request, view):
        sys_adm_subj = Subject.objects.prefetch_related('allowed_specialities').get(
            pk=SYSTEM_ADMINISTRATION_SUBJECT_ID
        )

        if request.user.role == UserRole.STUDENT:
            if (
                request.user.group.speciality
                in sys_adm_subj.allowed_specialities.all()
            ):
                return True
            return False
        else:
            if (
                sys_adm_subj in request.user.teacher_subjects.all()
            ):
                return True
            return False


class ReadOnlyIfTeacher(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS and request.user.role == UserRole.TEACHER
