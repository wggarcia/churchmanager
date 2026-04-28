from .models import ConfigPortal

def config(request):
    portal = ConfigPortal.objects.first()
    return {
        "config": portal,
        "igreja_nome": getattr(portal, "nome_igreja", "Igreja Evangélica"),
        "pastor_nome": getattr(portal, "pastor", "Pastor(a) responsável"),
        "nome_sistema": getattr(portal, "nome_sistema", "ChurchManager Pro"),
    }
