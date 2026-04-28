import json
from calendar import monthrange
from datetime import date

from django import template
from django.db.models import Sum
from django.utils.safestring import mark_safe

from core.models import (
    Contribuicao,
    Despesa,
    EscalaServico,
    Evento,
    Membro,
    Ministerio,
    PedidoOracao,
    Visitante,
)

register = template.Library()


@register.simple_tag
def church_dashboard_counts():
    """Retorna métricas rápidas para o dashboard customizado do admin."""
    return {
        "membros": Membro.objects.count(),
        "visitantes": Visitante.objects.count(),
        "ministerios": Ministerio.objects.count(),
        "eventos": Evento.objects.count(),
        "cultos": EscalaServico.objects.count(),
        "oracoes_total": PedidoOracao.objects.count(),
        "oracoes_pendentes": PedidoOracao.objects.filter(status=PedidoOracao.Status.PENDENTE).count(),
    }


@register.simple_tag
def church_financial_series(months=8):
    """Retorna labels e séries para gráfico financeiro do admin."""
    try:
        months = max(3, min(int(months), 18))
    except (TypeError, ValueError):
        months = 8

    today = date.today()
    labels, contrib, despesas = [], [], []

    for i in range(months - 1, -1, -1):
        year = today.year if today.month - i > 0 else today.year - 1
        month = (today.month - i - 1) % 12 + 1
        labels.append(f"{month:02d}/{year}")

        start = date(year, month, 1)
        end = date(year, month, monthrange(year, month)[1])

        total_contrib = (
            Contribuicao.objects.filter(data__range=(start, end)).aggregate(Sum("valor"))["valor__sum"] or 0
        )
        total_despesas = (
            Despesa.objects.filter(data__range=(start, end)).aggregate(Sum("valor"))["valor__sum"] or 0
        )

        contrib.append(float(total_contrib))
        despesas.append(float(total_despesas))

    payload = {"labels": labels, "contrib": contrib, "despesas": despesas}
    return mark_safe(json.dumps(payload))
