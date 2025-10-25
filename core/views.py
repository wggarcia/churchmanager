from datetime import date
from calendar import monthrange
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum

from .models import (
    Membro, Evento, Contribuicao, Despesa, Departamento,
    Visitante, Ministerio, EscalaServico, Missao, Banner
)

# -------------------- PÁGINAS PÚBLICAS --------------------
def index(request):
    """Página inicial do site"""
    eventos = Evento.objects.all().order_by('-data')[:12]
    banners = Banner.objects.filter(ativo=True).order_by('ordem')
    return render(request, "core/index.html", {"eventos": eventos, "banners": banners})


def eventos(request):
    """Página de eventos (mostra apenas os futuros)"""
    hoje = date.today()
    eventos = Evento.objects.filter(data__gte=hoje).order_by('data')
    return render(request, 'core/eventos.html', {'eventos': eventos})



# -------------------- LOGIN / LOGOUT --------------------
def login_view(request):
    """Tela de login"""
    if request.user.is_authenticated:
        return redirect("dashboard")

    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        error = "Usuário ou senha inválidos."

    return render(request, "core/login.html", {"error": error})


def logout_view(request):
    """Encerrar sessão"""
    logout(request)
    return render(request, "core/logout.html")


# -------------------- DASHBOARD --------------------
@login_required
def dashboard(request):
    """Painel administrativo"""
    ctx = {
        "membros_total": Membro.objects.count(),
        "visitantes_total": Visitante.objects.count(),
        "ministerios_total": Ministerio.objects.count(),
        "reunioes_total": EscalaServico.objects.count(),
    }
    return render(request, "core/dashboard.html", ctx)


# -------------------- PÁGINAS INTERNAS --------------------
@login_required
def membros(request):
    """Listagem de membros"""
    return render(request, "core/membros.html", {"membros": Membro.objects.all()})


@login_required
def visitantes(request):
    """Listagem de visitantes"""
    return render(request, "core/visitantes.html", {"visitantes": Visitante.objects.all()})


@login_required
def ministerios(request):
    """Listagem de ministérios"""
    return render(request, "core/ministerios.html", {"ministerios": Ministerio.objects.all()})


@login_required
def cultos(request):
    """Escala de Cultos"""
    escalas = EscalaServico.objects.prefetch_related("obreiros").all().order_by("-data")
    return render(request, "core/escala_obreiro.html", {"escalas": escalas})


@login_required
def missoes(request):
    """Página de missões"""
    missoes = Missao.objects.all().order_by('nome')
    return render(request, "core/missoes.html", {"missoes": missoes})


# -------------------- FINANCEIRO (APENAS SUPERUSER) --------------------
@user_passes_test(lambda u: u.is_superuser)
def financeiro(request):
    """Resumo financeiro e gráficos"""
    diz = Contribuicao.objects.filter(tipo="Dízimo").aggregate(Sum("valor"))["valor__sum"] or 0
    ofe = Contribuicao.objects.filter(tipo="Oferta").aggregate(Sum("valor"))["valor__sum"] or 0
    out = Contribuicao.objects.filter(tipo="Outros").aggregate(Sum("valor"))["valor__sum"] or 0
    dep = Despesa.objects.aggregate(Sum("valor"))["valor__sum"] or 0
    saldo = (diz + ofe + out) - dep

    hoje = date.today()
    labels, contrib_series, desp_series = [], [], []

    for i in range(11, -1, -1):
        ano = hoje.year if hoje.month - i > 0 else hoje.year - 1
        mes = (hoje.month - i - 1) % 12 + 1
        labels.append(f"{mes:02d}/{ano}")

        start = date(ano, mes, 1)
        end = date(ano, mes, monthrange(ano, mes)[1])
        c = Contribuicao.objects.filter(data__range=(start, end)).aggregate(Sum("valor"))["valor__sum"] or 0
        d = Despesa.objects.filter(data__range=(start, end)).aggregate(Sum("valor"))["valor__sum"] or 0

        contrib_series.append(float(c))
        desp_series.append(float(d))

    ctx = {
        "dizimos": float(diz),
        "ofertas": float(ofe),
        "outros": float(out),
        "despesas": float(dep),
        "saldo_atual": float(saldo),
        "labels": labels,
        "contrib_series": contrib_series,
        "desp_series": desp_series,
    }
    return render(request, "core/financeiro.html", ctx)
