from django.core.management.base import BaseCommand
from device.models import (
    Device,
    Relay,
    RelayGroup,
    RelayRelayGroupAssociation,
    RelaySchedule,
)
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from device.models import RelayGroup


class Command(BaseCommand):
    help = "Populate the database with sample data"

    def handle(self, *args, **options):
        def Group_creator(model):
            # Define the model and app name
            app_label = model._meta.app_label
            model_name = model._meta.model_name

            # Create the Group-permission group
            group_permission, created = Group.objects.get_or_create(
                name=f"{model_name}-permission"
            )

            if created:
                # Get content type for the RelayGroup model
                content_type = ContentType.objects.get(
                    app_label=app_label, model=model_name
                )

                # Define permissions for CRUD operations
                permissions = [
                    "add_" + model_name,
                    "change_" + model_name,
                    "delete_" + model_name,
                    "view_" + model_name,
                ]

                # Assign permissions to the Group-permission group
                for permission_codename in permissions:
                    permission, _ = Permission.objects.get_or_create(
                        codename=permission_codename,
                        content_type=content_type,
                    )
                    group_permission.permissions.add(permission)

                print(
                    f"Group '{model_name}-permission' created with CRUD permissions for RelayGroup."
                )
            else:
                print(f"Group '{model_name}-permission' already exists.")

        for each_model in [
            Device,
            Relay,
            RelayGroup,
            RelayRelayGroupAssociation,
            RelaySchedule,
        ]:
            Group_creator(each_model)
