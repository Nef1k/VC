from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker
from faker.providers import internet

from users.models import User


class Command(BaseCommand):
    @transaction.atomic()
    def handle(self, *args, **options):
        fake = Faker()
        fake.add_provider(internet)

        groups = Group.objects.all()
        raw_users = [
            (fake.user_name(), fake.email(), fake.bothify('#?###?##?#'))
            for i in range(0, len(groups))
        ]
        users = [
            User.objects.create_user(username=username, email=email, password=password)
            for username, email, password in raw_users
        ]

        for idx, user in enumerate(users):
            group = groups[idx]
            username = user.username
            _, _, password = raw_users[idx]

            user.groups.add(group)
            user.save()
            print(f'role: {group.name}; username: {username}; password: {password}')
