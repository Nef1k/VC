import logging

from django.core.management import BaseCommand
from faker import Faker
from faker.providers import internet

from contacts.models import Contact


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('n', nargs='?', type=int, default=10, help='Number of contacts to generate')

    def handle(self, *args, **options):
        logging.info(f'Generating {options["n"]} contacts...')

        contacts_number = options['n']
        contacts = self.generate_contacts(contacts_number)

        created = Contact.objects.bulk_create(contacts)
        logging.info(f'{len(created)} contacts created.')

    @staticmethod
    def generate_contacts(number):
        fake = Faker()
        fake.add_provider(internet)

        return [
            Contact(name=fake.name(), email=fake.ascii_free_email())
            for _ in range(0, number)
        ]
