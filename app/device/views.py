from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from device.mqtt_functions import client as mqtt_client


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from .models import Device, RelayGroup, Relay
from .serializers import DeviceSerializer, RelayGroupSerializer, RelaySerializer

from rest_framework import viewsets

class DeviceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

class RelayGroupViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = RelayGroup.objects.all()
    serializer_class = RelayGroupSerializer

class RelayViewSet(viewsets.ModelViewSet):
    """
    """
    queryset = Relay.objects.all()
    serializer_class = RelaySerializer

def publish_message(request):
    request_data = json.loads(request.body)
    rc, mid = mqtt_client.publish(request_data['topic'], request_data['msg'])
    return JsonResponse({'code': rc})