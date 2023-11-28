from django.contrib import admin

from .models import Device, Relay, RelayGroup, RelayRelayGroupAssociation, RelaySchedule


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device_type",
        "device_ip",
        "device_name",
        "extra",
        "is_on",
    )
    list_filter = ("is_on",)


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    list_display = ("id", "relay_pin", "is_on", "relay_name", "device")
    list_filter = ("is_on", "device")
    # raw_id_fields = ('relay_groups', 'relay_group_associations')


@admin.register(RelayGroup)
class RelayGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "group_name", "is_on")
    list_filter = ("is_on",)
    # raw_id_fields = ('relays',)


@admin.register(RelayRelayGroupAssociation)
class RelayRelayGroupAssociationAdmin(admin.ModelAdmin):
    list_display = ("id", "relay", "relay_group", "is_on")
    list_filter = ("relay", "relay_group", "is_on")


@admin.register(RelaySchedule)
class RelayScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "relay", "start_time", "end_time")
    list_filter = ("relay", "start_time", "end_time")
