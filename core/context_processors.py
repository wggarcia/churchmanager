# core/context_processors.py
from .models import ConfigPortal

def site_config(request):
    try:
        cfg = ConfigPortal.objects.first()
    except Exception:
        cfg = None

    return {
        "igreja_nome": cfg.nome if cfg else "Assembleia de Deus SJS",
        "igreja_logo": cfg.logo.url if cfg and cfg.logo else "/static/images/logo_default.png",
        "pastor_nome": cfg.pastor if cfg else "Pr. Responsável",
    }

