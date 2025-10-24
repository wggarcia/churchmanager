from django.core.management.base import BaseCommand
from core.models import ConfigPortal

class Command(BaseCommand):
    help = "Cria uma configuração padrão do portal se não existir."

    def handle(self, *args, **options):
        if not ConfigPortal.objects.exists():
            ConfigPortal.objects.create(
                nome_igreja="Assembleia de Deus Só Jesus Salva",
                pastor="Pastora Angélica Coutinho dos Santos",
                mensagem_boas_vindas="Bem-vindo ao portal da Assembleia de Deus Só Jesus Salva!",
            )
            self.stdout.write(self.style.SUCCESS("✅ Configuração padrão criada com sucesso!"))
        else:
            self.stdout.write(self.style.WARNING("⚠️ Já existe um ConfigPortal. Nenhuma ação necessária."))
