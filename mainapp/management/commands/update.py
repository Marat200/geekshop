from django.core.management import BaseCommand

from authapp.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = ShopUser.objects.all()
        for user in users:
            ShopUserProfile.objects.create(user=user)
