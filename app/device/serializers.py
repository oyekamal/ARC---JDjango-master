from rest_framework import serializers

from .models import Device, Relay, RelayGroup


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class RelayGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayGroup
        fields = "__all__"


class RelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Relay
        fields = "__all__"
