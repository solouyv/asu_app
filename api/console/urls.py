from rest_framework import routers
from api.console.views import (
    DeviceViewSet,
    CommandViewSet,
    ConnectToDeviceView,
    DisconnectFromDeviceView,
    ExecuteCommandView,
    web_gns_view,
)
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'commands', CommandViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('connect/', ConnectToDeviceView.as_view(), name='connect'),
    path('disconnect/', DisconnectFromDeviceView.as_view(), name='disconnect'),
    path('exec-command/', ExecuteCommandView.as_view(), name='exec-command'),
    path('web-gns/', web_gns_view, name='web-gns'),
]
