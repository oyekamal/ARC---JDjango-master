from django.shortcuts import render

# Create your views here.
import json
from django.http import JsonResponse
from device.mqtt_functions import client as mqtt_client


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions

from .models import Device, RelayGroup, Relay, RelaySchedule
from .serializers import DeviceSerializer, RelayGroupSerializer, RelaySerializer

from rest_framework import viewsets

# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .mqtt_functions import client

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import RelayForm, RelayGroupForm, RelayScheduleForm



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



class DeviceListView(ListView):
    model = Device
    template_name = 'device/device_list.html'
    context_object_name = 'devices'
    
from django.http import JsonResponse
from django.views import View

class ToggleDeviceView(View):
    def post(self, request, *args, **kwargs):
        device_id = request.POST.get('device_id')
        is_on = request.POST.get('is_on') == 'true'  # Convert 'true' string to boolean

        device = Device.objects.get(pk=device_id)
        device.is_on = is_on
        device.save()

        return JsonResponse({'status': 'success'})


class DeviceDeleteView(DeleteView):
    model = Device
    template_name = 'device/device_confirm_delete.html'
    success_url = reverse_lazy('device-list')




class RelayListView(ListView):
    model = Relay
    template_name = 'relay/relay_list.html'

class RelayUpdateView(UpdateView):
    model = Relay
    form_class = RelayForm
    template_name = 'relay/relay_edit.html'
    success_url = reverse_lazy('relay-list')

class RelayDeleteView(DeleteView):
    model = Relay
    template_name = 'relay/relay_confirm_delete.html'
    success_url = reverse_lazy('relay-list')



class RelayGroupListView(ListView):
    model = RelayGroup
    template_name = 'relaygroup/relaygroup_list.html'

class RelayGroupCreateView(CreateView):
    model = RelayGroup
    form_class = RelayGroupForm
    template_name = 'relaygroup/relaygroup_form.html'
    success_url = reverse_lazy('relaygroup-list')

class RelayGroupUpdateView(UpdateView):
    model = RelayGroup
    form_class = RelayGroupForm
    template_name = 'relaygroup/relaygroup_form.html'
    success_url = reverse_lazy('relaygroup-list')

class RelayGroupDeleteView(DeleteView):
    model = RelayGroup
    template_name = 'relaygroup/relaygroup_confirm_delete.html'
    success_url = reverse_lazy('relaygroup-list')



class RelayScheduleListView(ListView):
    model = RelaySchedule
    template_name = 'relayschedule/relayschedule_list.html'

class RelayScheduleCreateView(CreateView):
    model = RelaySchedule
    form_class = RelayScheduleForm
    template_name = 'relayschedule/relayschedule_form.html'
    success_url = reverse_lazy('relayschedule-list')

class RelayScheduleUpdateView(UpdateView):
    model = RelaySchedule
    form_class = RelayScheduleForm
    template_name = 'relayschedule/relayschedule_form.html'
    success_url = reverse_lazy('relayschedule-list')

class RelayScheduleDeleteView(DeleteView):
    model = RelaySchedule
    template_name = 'relayschedule/relayschedule_confirm_delete.html'
    success_url = reverse_lazy('relayschedule-list')
