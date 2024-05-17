# Generated by Django 4.2.6 on 2024-05-17 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("device", "0006_rule"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relay",
            name="device",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="relays",
                to="device.device",
            ),
        ),
        migrations.AlterField(
            model_name="relay",
            name="relay_group_associations",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="associated_relays",
                to="device.relayrelaygroupassociation",
            ),
        ),
        migrations.AlterField(
            model_name="relay",
            name="relay_groups",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="relays_in_group",
                to="device.relaygroup",
            ),
        ),
        migrations.AlterField(
            model_name="relaygroup",
            name="relays",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="groups", to="device.relay"
            ),
        ),
        migrations.AlterField(
            model_name="relayrelaygroupassociation",
            name="relay",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="group_associations",
                to="device.relay",
            ),
        ),
        migrations.AlterField(
            model_name="relayrelaygroupassociation",
            name="relay_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="associated_relay_groups",
                to="device.relaygroup",
            ),
        ),
        migrations.AlterField(
            model_name="relayschedule",
            name="relay",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="schedules",
                to="device.relay",
            ),
        ),
        migrations.CreateModel(
            name="RelayRelayAssociation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_on", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "relay",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="target_relays",
                        to="device.relay",
                    ),
                ),
                (
                    "relay_target",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="source_relays",
                        to="device.relay",
                    ),
                ),
            ],
        ),
    ]
