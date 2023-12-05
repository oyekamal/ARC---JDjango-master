# forms.py
import datetime as dt

from django import forms
from django.forms import Select

from .models import (Relay, RelayGroup, RelayRelayGroupAssociation,
                     RelaySchedule)


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
    HOUR_CHOICES = [(dt.time(hour=x), "{:02d}:00".format(x)) for x in range(0, 24)]
    start_time = forms.TimeField(widget=Select(choices=HOUR_CHOICES))
    end_time = forms.TimeField(widget=Select(choices=HOUR_CHOICES))

    class Meta:
        model = RelaySchedule
        fields = ["relay", "start_time", "end_time"]


class RelayRelayGroupAssociationForm(forms.ModelForm):
    class Meta:
        model = RelayRelayGroupAssociation
        fields = ["relay", "relay_group", "is_on"]
