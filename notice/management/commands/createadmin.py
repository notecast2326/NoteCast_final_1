from django.core.management.base import BaseCommand
from Notice.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args, **kwargs):

        if not CustomUser.objects.filter(email="admin@gmail.com").exists():

            CustomUser.objects.create_superuser(
                username="admin",
                email="admin@gmail.com",
                password="admin123"
            )

            print("Admin created")
        else:
            print("Admin already exists")