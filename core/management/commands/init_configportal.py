# core/management/commands/init_configportal.py
from django.core.management.base import BaseCommand
from core.models import ConfigPortal

class Command(BaseCommand):
    help = "Cria automaticamente o primeiro registro ConfigPortal se não existir"

    def handle(self, *args, **options):
        if not ConfigPortal.objects.exists():
            ConfigPortal.objects.create(
                nome="Assembleia de Deus SJS",
                pastor="Pr. Responsável",
            )
            self.stdout.write(self.style.SUCCESS("✅ ConfigPortal criado com sucesso."))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Já existe um ConfigPortal. Nenhuma ação necessária."))
