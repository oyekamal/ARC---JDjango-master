# Create your views here.
import json

from device.mqtt_functions import client as mqtt_client
# views.py
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .forms import (RelayForm, RelayGroupForm, RelayRelayGroupAssociationForm,
                    RelayScheduleForm)
from .models import (Device, Relay, RelayGroup, RelayRelayGroupAssociation,
                     RelaySchedule)
from .mqtt_functions import client
from .serializers import (DeviceSerializer, RelayGroupSerializer,
                          RelaySerializer)


def home(request):
    return render(request, "base.html")


class DeviceViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class RelayGroupViewSet(viewsets.ModelViewSet):
    """ """

    queryset = RelayGroup.objects.all()
    serializer_class = RelayGroupSerializer


class RelayViewSet(viewsets.ModelViewSet):
    """ """

    queryset = Relay.objects.all()
    serializer_class = RelaySerializer


def publish_message(request):
    try:
        # Ensure the JSON data is properly loaded, and keys are enclosed in double quotes
        device_info = json.loads(request.body.decode("utf-8"))

        # Check if 'device_name' is present in device_info
        if "device_name" in device_info:
            result = client.publish(device_info.get("device_name"), str(device_info))
            print("---------------- API start ----------------")
            print(device_info)
            print("---------------- API end ------------------")
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Missing 'device_name' in the request data",
                }
            )

    except json.JSONDecodeError as e:
        return JsonResponse(
            {"status": "error", "message": f"JSON decoding error: {str(e)}"}
        )


class DeviceListView(ListView):
    model = Device
    template_name = "device/device_list.html"
    context_object_name = "devices"


class ToggleDeviceView(View):
    def post(self, request, *args, **kwargs):
        id = request.POST.get("id")
        # Convert 'true' string to boolean
        is_on = request.POST.get("is_on") == "true"
        type = request.POST.get("type")
        print(type)
        if type == "device":
            device = Device.objects.get(pk=id)
            device.is_on = is_on
            device.save()
        elif type == "relay":
            relay = Relay.objects.get(pk=id)
            relay.is_on = is_on
            relay.save()

        elif type == "relaygroup":
            relay_group = RelayGroup.objects.get(pk=id)
            relay_group.is_on = is_on
            relay_group.save()

        elif type == "relay_group_association":
            relay_group_association = RelayRelayGroupAssociation.objects.get(pk=id)
            relay_group_association.is_on = is_on
            relay_group_association.save()

        elif type == "relayschedule":
            relayschedule = RelaySchedule.objects.get(pk=id)
            relayschedule.is_on = is_on
            relayschedule.save()

        return JsonResponse({"status": "success"})


class DeviceDeleteView(DeleteView):
    model = Device
    template_name = "device/device_confirm_delete.html"
    success_url = reverse_lazy("device-list")


class RelayListView(ListView):
    model = Relay
    template_name = "relay/relay_list.html"


class RelayUpdateView(UpdateView):
    model = Relay
    form_class = RelayForm
    template_name = "relay/relay_edit.html"
    success_url = reverse_lazy("relay-list")


class RelayDeleteView(DeleteView):
    model = Relay
    template_name = "relay/relay_confirm_delete.html"
    success_url = reverse_lazy("relay-list")


class RelayGroupListView(ListView):
    model = RelayGroup
    template_name = "relaygroup/relaygroup_list.html"


class RelayGroupCreateView(CreateView):
    model = RelayGroup
    form_class = RelayGroupForm
    template_name = "relaygroup/relaygroup_form.html"
    success_url = reverse_lazy("relaygroup-list")


class RelayGroupUpdateView(UpdateView):
    model = RelayGroup
    form_class = RelayGroupForm
    template_name = "relaygroup/relaygroup_form.html"
    success_url = reverse_lazy("relaygroup-list")


class RelayGroupDeleteView(DeleteView):
    model = RelayGroup
    template_name = "relaygroup/relaygroup_confirm_delete.html"
    success_url = reverse_lazy("relaygroup-list")


class RelayScheduleListView(ListView):
    model = RelaySchedule
    template_name = "relayschedule/relayschedule_list.html"


class RelayScheduleCreateView(CreateView):
    model = RelaySchedule
    form_class = RelayScheduleForm
    template_name = "relayschedule/relayschedule_form.html"
    success_url = reverse_lazy("relayschedule-list")


class RelayScheduleUpdateView(UpdateView):
    model = RelaySchedule
    form_class = RelayScheduleForm
    template_name = "relayschedule/relayschedule_form.html"
    success_url = reverse_lazy("relayschedule-list")


class RelayScheduleDeleteView(DeleteView):
    model = RelaySchedule
    template_name = "relayschedule/relayschedule_confirm_delete.html"
    success_url = reverse_lazy("relayschedule-list")


class RelayRelayGroupAssociationListView(ListView):
    model = RelayRelayGroupAssociation
    template_name = "relayrelaygroupassociations/relayrelaygroupassociation_list.html"


class RelayRelayGroupAssociationCreateView(CreateView):
    model = RelayRelayGroupAssociation
    form_class = RelayRelayGroupAssociationForm
    template_name = "relayrelaygroupassociations/relayrelaygroupassociation_form.html"
    success_url = reverse_lazy("relayrelaygroupassociation-list")


class RelayRelayGroupAssociationUpdateView(UpdateView):
    model = RelayRelayGroupAssociation
    form_class = RelayRelayGroupAssociationForm
    template_name = "relayrelaygroupassociations/relayrelaygroupassociation_form.html"
    success_url = reverse_lazy("relayrelaygroupassociation-list")


class RelayRelayGroupAssociationDeleteView(DeleteView):
    model = RelayRelayGroupAssociation
    template_name = (
        "relayrelaygroupassociations/relayrelaygroupassociation_confirm_delete.html"
    )
    success_url = reverse_lazy("relayrelaygroupassociation-list")
