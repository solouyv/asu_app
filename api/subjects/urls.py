from rest_framework import routers
from api.subjects.views import (
    SubjectViewSet,
    SemesterViewSet,
    LabViewSet,
    LectureViewSet,
    FolderViewSet,
    FileViewSet,
)
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'labs', LabViewSet)
router.register(r'lectures', LectureViewSet)
router.register(r'folders', FolderViewSet)
router.register(r'files', FileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
