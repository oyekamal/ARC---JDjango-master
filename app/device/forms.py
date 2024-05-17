# forms.py
import datetime as dt

from django import forms
from django.forms import Select

from .models import (
    Relay,
    RelayGroup,
    RelayRelayGroupAssociation,
    RelaySchedule,
    Rule,
    RelayRelayAssociation,
)

from django.forms import CheckboxSelectMultiple


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = "__all__"


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
    relays = forms.ModelMultipleChoiceField(
        queryset=Relay.objects.all(),
        widget=CheckboxSelectMultiple,
        required=False,  # Set to True if you want to make it a required field
    )

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


class RelayRelayGroupAssociationBehaviourForm(forms.ModelForm):
    class Meta:
        model = RelayRelayGroupAssociation
        fields = ["relay_group", "is_on"]


class RelayRelayAssociationBehaviourForm(forms.ModelForm):
    class Meta:
        model = RelayRelayAssociation
        fields = ["relay_target", "is_on"]
