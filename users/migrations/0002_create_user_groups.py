"""
Create Groups and link them with Permissions.

Groups are defined as `groups` dict where key is a name of the Group
and value is a list of Permissions that are to be added to the corresponding Group.

Example:
    >>> groups = {'regular': ['view_contact']}

"""
from django.contrib.auth.management import create_permissions
from django.db import migrations


groups = {
    'regular': [
        'view_contact',
    ],
    'admin': [
        'view_contact',
        'add_contact',
        'change_contact',
    ],
    'superuser': [
        'view_contact',
        'add_contact',
        'change_contact',
        'delete_contact',
    ],
}


def add_permissions(apps, schema_editor):
    apps.models_module = True
    create_permissions(apps, verbosity=0)
    apps.models_module = None


def create_user_groups(apps, schema_editor):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    known_permissions = {}

    for group_name, permissions in groups.items():
        group = Group(name=group_name)
        group.save()

        for permission_name in permissions:
            if permission_name not in known_permissions:
                known_permissions[permission_name] = Permission.objects\
                    .get(codename=permission_name)
            group.permissions.add(known_permissions[permission_name])
        group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_groups, migrations.RunPython.noop, atomic=True),
    ]
