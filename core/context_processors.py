from .models import ConfigPortal

def site_config(request):
    config = ConfigPortal.objects.first()
    return {
        "igreja_config": config,
        "igreja_nome": config.nome_igreja if config else "Igreja",
        "igreja_logo": config.logo.url if config and config.logo else None,
        "pastor_nome": config.pastor if config else "",
    }
