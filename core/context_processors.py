from .models import ConfigPortal

def site_config(request):
    cfg = ConfigPortal.objects.first()
    return {
        "igreja_nome": cfg.nome_igreja if cfg else "Assembleia de Deus Só Jesus Salva",
        "pastor_nome": cfg.pastor if cfg else "Pastora Angélica Coutinho dos Santos",
        "igreja_logo": (cfg.logo.url if (cfg and cfg.logo) else "/static/img/logo.png"),
        "mensagem_boas_vindas": (cfg.mensagem_boas_vindas if cfg else "Seja bem-vindo(a) ao nosso portal!"),
        "imagem_fundo": (cfg.imagem_fundo.url if (cfg and cfg.imagem_fundo) else None),
    }
