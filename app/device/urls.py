from django.urls import path
from . import views


from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'device', views.DeviceViewSet, basename="device")
router.register(r'relay_group', views.RelayGroupViewSet,
                basename="relay_group")
router.register(r'relay', views.RelayViewSet, basename="relay")


urlpatterns = [
    path("", views.home, name="home"),

    path('api', include(router.urls)),

    path('publish/', views.publish_message, name='publish'),
     path('devices/', views.DeviceListView.as_view(), name='device-list'),
    path('devices/<int:pk>/delete/', views.DeviceDeleteView.as_view(), name='device-delete'),
    
    path('toggle-device/', views.ToggleDeviceView.as_view(), name='toggle-device'),

    path('relays/', views.RelayListView.as_view(), name='relay-list'),
    path('relays/<int:pk>/edit/', views.RelayUpdateView.as_view(), name='relay-edit'),
    path('relays/<int:pk>/delete/', views.RelayDeleteView.as_view(), name='relay-delete'),

    path('relaygroups/', views.RelayGroupListView.as_view(), name='relaygroup-list'),
    path('relaygroups/create/', views.RelayGroupCreateView.as_view(), name='relaygroup-create'),
    path('relaygroups/<int:pk>/edit/', views.RelayGroupUpdateView.as_view(), name='relaygroup-edit'),
    path('relaygroups/<int:pk>/delete/', views.RelayGroupDeleteView.as_view(), name='relaygroup-delete'),

    path('relayschedules/', views.RelayScheduleListView.as_view(), name='relayschedule-list'),
    path('relayschedules/create/', views.RelayScheduleCreateView.as_view(), name='relayschedule-create'),
    path('relayschedules/<int:pk>/edit/', views.RelayScheduleUpdateView.as_view(), name='relayschedule-edit'),
    path('relayschedules/<int:pk>/delete/', views.RelayScheduleDeleteView.as_view(), name='relayschedule-delete'),

]
