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

from .forms import (
    RelayForm,
    RelayGroupForm,
    RelayRelayGroupAssociationForm,
    RelayScheduleForm,
)
from .models import Device, Relay, RelayGroup, RelayRelayGroupAssociation, RelaySchedule
from .mqtt_functions import client
from .serializers import DeviceSerializer, RelayGroupSerializer, RelaySerializer
from django.contrib.auth.mixins import PermissionRequiredMixin


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
            result = client.publish(device_info.get(
                "device_name"), str(device_info))
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


class DeviceListView(PermissionRequiredMixin, ListView):
    model = Device
    template_name = "device/device_list.html"
    context_object_name = "devices"
    permission_required = "device.view_device"


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
            relay_group_association = RelayRelayGroupAssociation.objects.get(
                pk=id)
            relay_group_association.is_on = is_on
            relay_group_association.save()

        elif type == "relayschedule":
            relayschedule = RelaySchedule.objects.get(pk=id)
            relayschedule.is_on = is_on
            relayschedule.save()

        return JsonResponse({"status": "success"})


class DeviceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Device
    template_name = "device/device_confirm_delete.html"
    success_url = reverse_lazy("device-list")
    permission_required = "device.delete_device"


class RelayListView(PermissionRequiredMixin, ListView):
    model = Relay
    template_name = "relay/relay_list.html"
    permission_required = "device.view_relay"


class RelayUpdateView(PermissionRequiredMixin, UpdateView):
    model = Relay
    form_class = RelayForm
    template_name = "relay/relay_edit.html"
    success_url = reverse_lazy("relay-list")
    permission_required = "device.change_relay"


class RelayDeleteView(PermissionRequiredMixin, DeleteView):
    model = Relay
    template_name = "relay/relay_confirm_delete.html"
    success_url = reverse_lazy("relay-list")
    permission_required = "device.delete_relay"


class RelayGroupListView(PermissionRequiredMixin, ListView):
    model = RelayGroup
    template_name = "relaygroup/relaygroup_list.html"
    permission_required = "device.view_relaygroup"


class RelayGroupCreateView(PermissionRequiredMixin, CreateView):
    model = RelayGroup
    form_class = RelayGroupForm
    template_name = "relaygroup/relaygroup_form.html"
    success_url = reverse_lazy("relaygroup-list")
    permission_required = "device.add_relaygroup"


class RelayGroupUpdateView(PermissionRequiredMixin, UpdateView):
    model = RelayGroup
    form_class = RelayGroupForm
    template_name = "relaygroup/relaygroup_form.html"
    success_url = reverse_lazy("relaygroup-list")
    permission_required = "device.change_relaygroup"


class RelayGroupDeleteView(PermissionRequiredMixin, DeleteView):
    model = RelayGroup
    template_name = "relaygroup/relaygroup_confirm_delete.html"
    success_url = reverse_lazy("relaygroup-list")
    permission_required = "device.delete_relaygroup"


class RelayScheduleListView(PermissionRequiredMixin, ListView):
    model = RelaySchedule
    template_name = "relayschedule/relayschedule_list.html"
    permission_required = "device.view_relayschedule"


class RelayScheduleCreateView(PermissionRequiredMixin, CreateView):
    model = RelaySchedule
    form_class = RelayScheduleForm
    template_name = "relayschedule/relayschedule_form.html"
    success_url = reverse_lazy("relayschedule-list")
    permission_required = "device.add_relayschedule"


class RelayScheduleUpdateView(PermissionRequiredMixin, UpdateView):
    model = RelaySchedule
    form_class = RelayScheduleForm
    template_name = "relayschedule/relayschedule_form.html"
    success_url = reverse_lazy("relayschedule-list")
    permission_required = "device.change_relayschedule"


class RelayScheduleDeleteView(PermissionRequiredMixin, DeleteView):
    model = RelaySchedule
    template_name = "relayschedule/relayschedule_confirm_delete.html"
    success_url = reverse_lazy("relayschedule-list")
    permission_required = "device.delete_relayschedule"


class RelayRelayGroupAssociationListView(PermissionRequiredMixin, ListView):
    model = RelayRelayGroupAssociation
    template_name = "relayrelaygroupassociations/relayrelaygroupassociation_list.html"
    permission_required = "device.delete_relayrelaygroupassociation"


class RelayRelayGroupAssociationCreateView(PermissionRequiredMixin, CreateView):
    model = RelayRelayGroupAssociation
    form_class = RelayRelayGroupAssociationForm
    template_name = "relayrelaygroupassociations/relayrelaygroupassociation_form.html"
    success_url = reverse_lazy("relayrelaygroupassociation-list")
    permission_required = "device.delete_relayrelaygroupassociation"


class RelayRelayGroupAssociationUpdateView(PermissionRequiredMixin, UpdateView):
    model = RelayRelayGroupAssociation
    form_class = RelayRelayGroupAssociationForm
    template_name = "relayrelaygroupassociations/relayrelaygroupassociation_form.html"
    success_url = reverse_lazy("relayrelaygroupassociation-list")
    permission_required = "device.delete_relayrelaygroupassociation"


class RelayRelayGroupAssociationDeleteView(PermissionRequiredMixin, DeleteView):
    model = RelayRelayGroupAssociation
    template_name = (
        "relayrelaygroupassociations/relayrelaygroupassociation_confirm_delete.html"
    )
    success_url = reverse_lazy("relayrelaygroupassociation-list")
    permission_required = "device.delete_relayrelaygroupassociation"


def error_404_view(request, exception=None):
    return render(request, "device/error.html", {'message': "404", "detail": "Not Found"})


def error_500_view(request, exception=None):
    return render(request, "device/error.html", {'message': "500", "detail": "Internal Server Error"})


def error_403_view(request, exception=None):
    return render(request, "device/error.html", {'message': "403", "detail": "Not allowed"})


def error_400_view(request, exception=None):
    return render(request, "device/error.html", {'message': "400", "detail": "Client-side error"})
