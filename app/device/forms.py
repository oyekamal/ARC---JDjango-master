# forms.py
from django import forms
from .models import Relay, RelayGroup

class RelayForm(forms.ModelForm):
    class Meta:
        model = Relay
        fields = ['relay_pin', 'is_on', 'relay_name', 'device', 'relay_groups', 'relay_group_associations']



class RelayGroupForm(forms.ModelForm):
    class Meta:
        model = RelayGroup
        fields = ['group_name', 'is_on', 'relays']
