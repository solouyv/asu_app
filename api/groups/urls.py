from rest_framework import routers
from api.groups.views import GroupViewSet, SpecialityViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'specialities', SpecialityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
