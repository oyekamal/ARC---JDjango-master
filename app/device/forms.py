# forms.py
from django import forms
from .models import Relay, RelayGroup, RelaySchedule, RelayRelayGroupAssociation


class RelayForm(forms.ModelForm):
    class Meta:
        model = Relay
        fields = [
            "relay_pin",
            "is_on",
            "relay_name",
            "device",
            "relay_groups",
            "relay_group_associations",
        ]


class RelayGroupForm(forms.ModelForm):
    class Meta:
        model = RelayGroup
        fields = ["group_name", "is_on", "relays"]


class RelayScheduleForm(forms.ModelForm):
    class Meta:
        model = RelaySchedule
        fields = ["relay", "start_time", "end_time"]


class RelayRelayGroupAssociationForm(forms.ModelForm):
    class Meta:
        model = RelayRelayGroupAssociation
        fields = ["relay", "relay_group", "is_on"]
