from datetime import date
from calendar import monthrange
import re
from urllib.parse import quote
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from .models import AnotacaoAdmin

from .models import (
    ConfigPortal, Membro, Evento, Contribuicao, Despesa,
    Visitante, Ministerio, EscalaServico, Missao, Banner, PedidoOracao
)

# -------------------- PÁGINAS PÚBLICAS --------------------
def index(request):
    """Página inicial do site"""
    hoje = date.today()
    eventos = Evento.objects.order_by("-data")[:12]
    proximos_eventos = Evento.objects.filter(data__gte=hoje).order_by("data")[:3]
    banners = Banner.objects.filter(ativo=True).order_by("ordem")
    config = ConfigPortal.objects.first()

    agenda_texto = getattr(config, "agenda_cultos", "") or ""
    dias_culto = [linha.strip() for linha in agenda_texto.splitlines() if linha.strip()]

    if not dias_culto:
        dias_semana_pt = {
            0: "Segunda-feira",
            1: "Terça-feira",
            2: "Quarta-feira",
            3: "Quinta-feira",
            4: "Sexta-feira",
            5: "Sábado",
            6: "Domingo",
        }
        proximas_escalas = EscalaServico.objects.filter(data__gte=hoje).order_by("data")[:5]
        dias_culto = [
            f"{dias_semana_pt.get(escala.data.weekday(), 'Dia')} • {escala.data.strftime('%d/%m')} • {escala.culto}"
            for escala in proximas_escalas
        ]

    return render(
        request,
        "core/index.html",
        {
            "eventos": eventos,
            "banners": banners,
            "proximos_eventos": proximos_eventos,
            "dias_culto": dias_culto,
            "metricas": {
                "membros": Membro.objects.count(),
                "visitantes": Visitante.objects.count(),
                "ministerios": Ministerio.objects.count(),
                "cultos": EscalaServico.objects.count(),
            },
        },
    )


def eventos(request):
    """Lista apenas eventos de hoje em diante, ordenados por data"""
    hoje = date.today()
    eventos = Evento.objects.filter(data__gte=hoje).order_by('data')
    return render(request, 'core/eventos.html', {'eventos': eventos, 'hoje': hoje})



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
        "eventos_total": Evento.objects.count(),
        "pedidos_oracao_total": PedidoOracao.objects.count(),
        "pedidos_oracao_pendentes": PedidoOracao.objects.filter(status=PedidoOracao.Status.PENDENTE).count(),
    }
    return render(request, "core/dashboard.html", ctx)


# -------------------- PÁGINAS INTERNAS --------------------
@login_required
def membros(request):
    """Listagem de membros"""
    return render(request, "core/membros.html", {"membros": Membro.objects.order_by("nome")})


@login_required
def visitantes(request):
    """Listagem de visitantes"""
    return render(request, "core/visitantes.html", {"visitantes": Visitante.objects.order_by("-data_visita")})


@login_required
def ministerios(request):
    """Listagem de ministérios"""
    return render(request, "core/ministerios.html", {"ministerios": Ministerio.objects.order_by("nome")})


def cultos(request):
    """Escala de Cultos"""
    escalas = EscalaServico.objects.prefetch_related("obreiros").all().order_by("-data")
    return render(request, "core/escala_obreiro.html", {"escalas": escalas})


def missoes(request):
    """Página de missões"""
    missoes = Missao.objects.all().order_by('nome')
    return render(request, "core/missoes.html", {"missoes": missoes})


def pedido_oracao(request):
    """Recebe pedidos de oração públicos."""
    config = ConfigPortal.objects.first()
    whatsapp_destino = getattr(config, "whatsapp_pedidos_oracao", None) or getattr(config, "telefone_contato", None)
    whatsapp_digits = re.sub(r"\D", "", whatsapp_destino or "")
    sucesso = False
    if request.method == "POST":
        nome = (request.POST.get("nome") or "").strip() or None
        telefone = (request.POST.get("telefone") or "").strip() or None
        email = (request.POST.get("email") or "").strip() or None
        pedido = (request.POST.get("pedido") or "").strip()
        confidencial = request.POST.get("confidencial") == "on"

        if pedido:
            PedidoOracao.objects.create(
                nome=nome,
                telefone=telefone,
                email=email,
                pedido=pedido,
                confidencial=confidencial,
            )
            sucesso = True
            if whatsapp_digits:
                texto = (
                    "Novo pedido de oração recebido pelo site:\n"
                    f"Nome: {nome or 'Não informado'}\n"
                    f"Telefone: {telefone or 'Não informado'}\n"
                    f"E-mail: {email or 'Não informado'}\n"
                    f"Confidencial: {'Sim' if confidencial else 'Não'}\n"
                    f"Pedido: {pedido}"
                )
                whatsapp_url = f"https://wa.me/{whatsapp_digits}?text={quote(texto)}"
                return redirect(whatsapp_url)

    return render(
        request,
        "core/pedido_oracao.html",
        {
            "sucesso": sucesso,
            "whatsapp_ativo": bool(whatsapp_digits),
            "whatsapp_numero": whatsapp_digits,
        },
    )


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

@login_required
def bloco_notas(request):
    anotacoes = AnotacaoAdmin.objects.order_by("-atualizado_em")
    return render(request, "core/bloco_notas.html", {
        "anotacoes": anotacoes
    })
