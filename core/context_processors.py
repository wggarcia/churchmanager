# core/context_processors.py
from django.conf import settings

def site_config(request):
    """
    Carrega as informações do portal (nome da igreja, pastor, logo, banner, etc.)
    Evita erro 500 se o banco ainda não estiver pronto.
    """
    try:
        from .models import ConfigPortal
        cfg = ConfigPortal.objects.first()
    except Exception:
        cfg = None

    default_logo = settings.STATIC_URL + "images/logo.png"
    default_banner = settings.STATIC_URL + "images/banner_principal.jpg"

    return {
        "igreja_nome": cfg.nome_igreja if cfg else "Assembleia de Deus Só Jesus Salva",
        "pastor_nome": cfg.pastor if cfg else "Pr. Responsável",
        "igreja_logo": cfg.logo.url if cfg and cfg.logo else default_logo,
        "igreja_banner": cfg.banner.url if cfg and cfg.banner else default_banner,
        "mensagem_boas_vindas": cfg.mensagem_boas_vindas if cfg else "Bem-vindo ao nosso portal!",
        "banner_titulo": cfg.banner_titulo if cfg else "",
        "banner_subtitulo": cfg.banner_subtitulo if cfg else "",
    }
