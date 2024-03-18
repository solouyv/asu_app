from rest_framework import routers
from api.simple_tests.views import (
    TestViewSet,
    TestResultViewSet,
)
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'tests-results', TestResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
