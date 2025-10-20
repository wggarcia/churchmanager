from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ConfigPortal, Membro, Ministerio, Departamento, Evento,
    Contribuicao, Despesa, Missao, Visitante, ReuniaoMinisterial
)

admin.site.site_header = "Painel Administrativo ADSJS"
admin.site.site_title = "Gestão da Igreja ADSJS"
admin.site.index_title = "Bem-vindo ao painel"

@admin.register(ConfigPortal)
class ConfigPortalAdmin(admin.ModelAdmin):
    list_display = ("nome_igreja", "pastor", "logo_preview")
    readonly_fields = ("logo_preview",)
    fieldsets = (
        ("Identidade", {"fields": ("nome_igreja", "pastor", "logo", "logo_preview")}),
        ("Portal", {"fields": ("mensagem_boas_vindas", "imagem_fundo")}),
    )
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:70px;border-radius:8px;">', obj.logo.url)
        return "—"
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
    list_display = ("tipo", "valor", "data", "contribuinte")
    list_filter = ("tipo", "data")
    search_fields = ("contribuinte",)

@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ("descricao", "valor", "data")
    list_filter = ("data",)
    search_fields = ("descricao",)

@admin.register(Missao)
class MissaoAdmin(admin.ModelAdmin):
    list_display = ("nome",)

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ("nome", "data_visita")
    list_filter = ("data_visita",)

@admin.register(ReuniaoMinisterial)
class ReuniaoMinisterialAdmin(admin.ModelAdmin):
    list_display = ("titulo", "data")
