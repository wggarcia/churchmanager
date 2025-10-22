# core/admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    ConfigPortal, Membro, Ministerio, Departamento, Evento,
    Contribuicao, Despesa, Missao, Visitante,
    Obreiro, EscalaServico
)

@admin.register(ConfigPortal)
class ConfigPortalAdmin(admin.ModelAdmin):
    list_display = ("nome_igreja", "pastor", "logo_preview")
    readonly_fields = ("logo_preview",)

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" style="height:60px;">')
        return "Sem logo"
    logo_preview.short_description = "Prévia da Logo"


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "batizado")
    search_fields = ("nome", "telefone", "email")


@admin.register(Ministerio)
class MinisterioAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao")


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "ministerio")


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "data")
    search_fields = ("titulo",)


@admin.register(Contribuicao)
class ContribuicaoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "valor", "data", "contribuinte", "outros_destino")
    list_filter = ("tipo", "data")
    search_fields = ("contribuinte", "outros_destino")


@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ("descricao", "valor", "data", "recibo")
    list_filter = ("data",)
    search_fields = ("descricao",)


@admin.register(Missao)
class MissaoAdmin(admin.ModelAdmin):
    list_display = ("nome",)


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ("nome", "data_visita", "frequenta_igreja", "igreja_origem", "telefone", "email")
    list_filter = ("frequenta_igreja", "data_visita")
    search_fields = ("nome", "igreja_origem", "telefone", "email")


@admin.register(Obreiro)
class ObreiroAdmin(admin.ModelAdmin):
    list_display = ("nome", "cargo", "telefone", "email")
    list_filter = ("cargo",)
    search_fields = ("nome", "telefone", "email")


@admin.register(EscalaServico)
class EscalaServicoAdmin(admin.ModelAdmin):
    list_display = ("data", "culto")
    filter_horizontal = ("obreiros",)

# Ajusta títulos do admin com base em ConfigPortal
try:
    cfg = ConfigPortal.objects.first()
    if cfg:
        admin.site.site_header = f"{cfg.nome_igreja} — Painel Administrativo"
    else:
        admin.site.site_header = "ADSJS — Painel Administrativo"
except Exception:
    admin.site.site_header = "ADSJS — Painel Administrativo"

admin.site.site_title = "Gestão da Igreja ADSJS"
admin.site.index_title = "Painel Administrativo"
