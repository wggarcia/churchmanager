from .models import ConfigPortal

def config(request):
    try:
        return {'config': ConfigPortal.objects.first()}
    except:
        return {'config': None}
