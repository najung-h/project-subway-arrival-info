from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
import os

class Command(BaseCommand):
    help = "Create/Update Google SocialApp and Site domain from env"

    def handle(self, *args, **kwargs):
        domain = os.getenv("SITE_DOMAIN", "localhost:8000")
        site, _ = Site.objects.get_or_create(id=getattr(settings, "SITE_ID", 1))
        site.domain = domain
        site.name = domain
        site.save()
        self.stdout.write(self.style.SUCCESS(f"[Site] {site.domain}"))

        client_id = os.getenv("GOOGLE_CLIENT_ID")
        secret = os.getenv("GOOGLE_CLIENT_SECRET")
        if not client_id or not secret:
            self.stdout.write(self.style.WARNING("GOOGLE_CLIENT_* not set"))
            return

        app, _ = SocialApp.objects.get_or_create(provider="google", name="Google")
        app.client_id = client_id
        app.secret = secret
        app.save()
        app.sites.set([site])
        self.stdout.write(self.style.SUCCESS("[SocialApp] Google configured"))
