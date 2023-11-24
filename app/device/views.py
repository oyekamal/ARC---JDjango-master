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

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .mqtt_functions import client


def home(request):
    return render(request, "base.html")


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
    try:
        # Ensure the JSON data is properly loaded, and keys are enclosed in double quotes
        device_info = json.loads(request.body.decode('utf-8'))

        # Check if 'device_name' is present in device_info
        if 'device_name' in device_info:
            result = client.publish(device_info.get(
                'device_name'), str(device_info))
            print(device_info)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "Missing 'device_name' in the request data"})

    except json.JSONDecodeError as e:
        return JsonResponse({"status": "error", "message": f"JSON decoding error: {str(e)}"})
