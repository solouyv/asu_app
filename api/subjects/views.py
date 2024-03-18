from rest_framework import viewsets
from api.subjects.models import Subject, Semester, Lecture, Lab, Folder, File
from api.subjects.serializers import (
    SubjectSerializer,
    SemesterSerializer,
    LabSerializer,
    LectureSerializer,
    FolderSerializer,
    FileSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from asu_app.custom_permissions import ReadOnly
from api.users.models import UserRole


class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Subject.objects.all()
        if self.request.user.role == UserRole.STUDENT:
            return (
                Subject.objects
                .filter(allowed_specialities__groups__in=[self.request.user.group])  # noqa
                .all().prefetch_related('allowed_specialities__groups')
            )
        else:
            return (
                Subject.objects
                .filter(id__in=[s.id for s in self.request.user.teacher_subjects.all()])  # noqa
                .all().prefetch_related('allowed_specialities')
            )


class SemesterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = Semester.objects.all().select_related('subject')
    serializer_class = SemesterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subject']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Semester.objects.all().select_related('subject')
        if self.request.user.role == UserRole.STUDENT:
            return (
                Semester.objects
                .filter(subject__allowed_specialities__groups__in=[self.request.user.group])
                .all().prefetch_related('subject__allowed_specialities__groups')
            )
        else:
            return (
                Semester.objects
                .filter(subject__id__in=[s.id for s in self.request.user.teacher_subjects.all()])
                .all().prefetch_related('subject__allowed_specialities')
            )


class LabViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = Lab.objects.all().select_related('semester__subject')
    serializer_class = LabSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['semester']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Lab.objects.all().select_related('semester__subject')
        if self.request.user.role == UserRole.STUDENT:
            return (
                Lab.objects
                .filter(semester__subject__allowed_specialities__groups__in=[self.request.user.group])
                .all().prefetch_related('semester__subject__allowed_specialities__groups')
            )
        else:
            return (
                Lab.objects
                .filter(semester__subject__id__in=[s.id for s in self.request.user.teacher_subjects.all()])
                .all().prefetch_related('semester__subject__allowed_specialities')
            )


class LectureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = Lecture.objects.all().select_related('semester__subject')
    serializer_class = LectureSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['semester']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Lecture.objects.all().select_related('semester__subject')
        if self.request.user.role == UserRole.STUDENT:
            return (
                Lecture.objects
                .filter(semester__subject__allowed_specialities__groups__in=[self.request.user.group])
                .all().prefetch_related('semester__subject__allowed_specialities__groups')
            )
        else:
            return (
                Lecture.objects
                .filter(semester__subject__id__in=[s.id for s in self.request.user.teacher_subjects.all()])
                .all().prefetch_related('semester__subject__allowed_specialities')
            )


class FolderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = Folder.objects.all().select_related('semester__subject')
    serializer_class = FolderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['semester']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Folder.objects.all().select_related('semester__subject')
        if self.request.user.role == UserRole.STUDENT:
            return (
                Folder.objects
                .filter(semester__subject__allowed_specialities__groups__in=[self.request.user.group])
                .all().prefetch_related('semester__subject__allowed_specialities__groups')
            )
        else:
            return (
                Folder.objects
                .filter(semester__subject__id__in=[s.id for s in self.request.user.teacher_subjects.all()])
                .all().prefetch_related('semester__subject__allowed_specialities')
            )


class FileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser | ReadOnly]
    queryset = File.objects.all().select_related('folder__semester__subject')
    serializer_class = FileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['folder']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return File.objects.all().select_related('folder__semester__subject')
        if self.request.user.role == UserRole.STUDENT:
            return (
                File.objects
                .filter(folder__semester__subject__allowed_specialities__groups__in=[self.request.user.group])
                .all().prefetch_related('folder__semester__subject__allowed_specialities__groups')
            )
        else:
            return (
                File.objects
                .filter(folder__semester__subject__id__in=[s.id for s in self.request.user.teacher_subjects.all()])
                .all().prefetch_related('folder__semester__subject__allowed_specialities')
            )
