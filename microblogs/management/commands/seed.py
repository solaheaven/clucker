from django.core.management.base import BaseCommand, CommandError
from faker import Faker
class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
    def handle(self, *args, **opttions):
        print("WARNING: The SEED command has not implemented yet.")
