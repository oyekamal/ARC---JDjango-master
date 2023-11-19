from django.urls import path
from . import views


from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'device', views.DeviceViewSet,basename="device")
router.register(r'relay_group', views.RelayGroupViewSet,basename="relay_group")
router.register(r'relay', views.RelayViewSet,basename="relay")


urlpatterns = [
        path('', include(router.urls)),

    path('publish', views.publish_message, name='publish'),
]