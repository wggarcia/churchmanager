from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from .models import (
    Membro, Evento, Contribuicao, Despesa,
    Departamento, Visitante, Missao, ReuniaoMinisterial
)

def index(request):
    context = {
        "membros": Membro.objects.all(),
        "eventos": Evento.objects.all().order_by("-data")[:6],
    }
    return render(request, "core/home.html", context)

def membros(request):
    return render(request, "core/membros.html", {"membros": Membro.objects.all()})

def eventos(request):
    return render(request, "core/eventos.html", {"eventos": Evento.objects.all().order_by("-data")})

def visitantes(request):
    return render(request, "core/visitantes.html", {"visitantes": Visitante.objects.all().order_by("-data_visita")})

def reunioes(request):
    return render(request, "core/reunioes.html", {"reunioes": ReuniaoMinisterial.objects.all().order_by("-data")})

def missoes(request):
    return render(request, "core/missoes.html", {"missoes": Missao.objects.all()})

@user_passes_test(lambda u: u.is_superuser)
def financeiro(request):
    dizimos = Contribuicao.objects.filter(tipo="Dízimo").aggregate(total=Sum("valor"))["total"] or 0
    ofertas = Contribuicao.objects.filter(tipo="Oferta").aggregate(total=Sum("valor"))["total"] or 0
    outros  = Contribuicao.objects.filter(tipo="Outros").aggregate(total=Sum("valor"))["total"] or 0
    despesas = Despesa.objects.aggregate(total=Sum("valor"))["total"] or 0
    saldo_atual = (dizimos + ofertas + outros) - despesas

    context = {
        "dizimos": dizimos,
        "ofertas": ofertas,
        "outros": outros,
        "despesas": despesas,
        "saldo_atual": saldo_atual,
    }
    return render(request, "core/financeiro.html", context)
