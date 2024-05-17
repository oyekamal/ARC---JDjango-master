from django.db import models

# Assuming IF_WHEN_CHOICES, EVENT_CHOICES, ACTION_CHOICES, TARGET_CHOICES are defined above
IF_WHEN_CHOICES = [
    ("If", "If"),
    ("When", "When"),
]
EVENT_CHOICES = [
    ("Schedule", "Schedule"),
    ("Relay State Change", "Relay State Change"),
    # ('Button Press', 'Button Press'),
    # ('Zone Change', 'Zone Change'),
]
ACTION_CHOICES = [
    ("On", "On"),
    ("Off", "Off"),
    ("Toggle", "Toggle"),
    ("Dim", "Dim"),
    ("Lockout", "Lockout"),
]
TARGET_CHOICES = [
    ("Group", "Group"),
    ("Relay", "Relay"),
]


class Rule(models.Model):
    if_when = models.CharField(max_length=50, choices=IF_WHEN_CHOICES)
    event = models.CharField(max_length=50, choices=EVENT_CHOICES)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target = models.CharField(max_length=50, choices=TARGET_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.if_when} - {self.event} - {self.action} - {self.target}"


class Device(models.Model):
    device_type = models.CharField(max_length=255, null=True)
    device_ip = models.CharField(max_length=255, null=True)
    device_name = models.CharField(max_length=255, null=True)
    extra = models.JSONField(null=True)
    is_on = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.device_name)


class Relay(models.Model):
    relay_pin = models.IntegerField()
    is_on = models.BooleanField(default=False)
    relay_name = models.CharField(max_length=255, null=True)
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, null=True, related_name="relays"
    )
    relay_groups = models.ManyToManyField(
        "RelayGroup", null=True, blank=True, related_name="relays_in_group"
    )
    relay_group_associations = models.ManyToManyField(
        "RelayRelayGroupAssociation",
        related_name="associated_relays",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Relay {self.relay_name}"


class RelayGroup(models.Model):
    group_name = models.CharField(max_length=255, unique=True)
    is_on = models.BooleanField(default=True)
    relays = models.ManyToManyField(Relay, null=True, blank=True, related_name="groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.group_name)


class RelayRelayGroupAssociation(models.Model):
    relay = models.ForeignKey(
        Relay, on_delete=models.CASCADE, null=True, related_name="group_associations"
    )
    relay_group = models.ForeignKey(
        RelayGroup,
        on_delete=models.CASCADE,
        related_name="associated_relay_groups",
        null=True,
        blank=True,
    )
    is_on = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RelayRelayGroupAssociation({self.relay}, {self.relay_group})"


class RelayRelayAssociation(models.Model):
    relay = models.ForeignKey(
        Relay, on_delete=models.CASCADE, null=True, related_name="target_relays"
    )
    relay_target = models.ForeignKey(
        Relay, on_delete=models.CASCADE, null=True, related_name="source_relays"
    )
    is_on = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RelayRelayAssociation({self.relay}, {self.relay_target})"


class RelaySchedule(models.Model):
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE, related_name="schedules")
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_on = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Relay Schedule for {self.relay.relay_name}"
