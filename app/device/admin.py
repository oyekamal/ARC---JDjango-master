from django.contrib import admin

from .models import (
    Rule,
    Device,
    Relay,
    RelayGroup,
    RelayRelayGroupAssociation,
    RelayRelayAssociation,
    RelaySchedule,
)


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "if_when",
        "event",
        "action",
        "target",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "device_type",
        "device_ip",
        "device_name",
        "extra",
        "is_on",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_on", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(Relay)
class RelayAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "relay_pin",
        "is_on",
        "relay_name",
        "device",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_on", "device", "created_at", "updated_at")
    raw_id_fields = ("relay_groups", "relay_group_associations")
    date_hierarchy = "created_at"


@admin.register(RelayGroup)
class RelayGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "group_name", "is_on", "created_at", "updated_at")
    list_filter = ("is_on", "created_at", "updated_at")
    raw_id_fields = ("relays",)
    date_hierarchy = "created_at"


@admin.register(RelayRelayGroupAssociation)
class RelayRelayGroupAssociationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "relay",
        "relay_group",
        "is_on",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "relay",
        "relay_group",
        "is_on",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"


@admin.register(RelayRelayAssociation)
class RelayRelayAssociationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "relay",
        "relay_target",
        "is_on",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "relay",
        "relay_target",
        "is_on",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"


@admin.register(RelaySchedule)
class RelayScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "relay",
        "start_time",
        "end_time",
        "is_on",
        "created_at",
        "updated_at",
    )
    list_filter = ("relay", "is_on", "created_at", "updated_at")
    date_hierarchy = "created_at"
