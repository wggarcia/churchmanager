from django.contrib import admin
from .models import (
    ConfigPortal, Membro, Obreiro, Departamento, Evento,
    Contribuicao, Despesa, Ministerio, Visitante,
    EscalaServico, Missao, Banner
)

# -------------------- CONFIGURAÇÃO DO PORTAL --------------------
@admin.register(ConfigPortal)
class ConfigPortalAdmin(admin.ModelAdmin):
    list_display = ("nome_igreja", "pastor", "atualizado_em")
    fieldsets = (
        ("Informações da Igreja", {
            "fields": ("nome_igreja", "pastor", "mensagem_boas_vindas"),
            "description": "Configurações gerais do portal."
        }),
        ("Imagens do Site", {
            "fields": ("logo", "plano_fundo"),
            "description": "Logo e plano de fundo exibidos no site."
        }),
    )


# -------------------- MEMBROS --------------------
@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "batizado", "cargo")
    search_fields = ("nome", "email")
    list_filter = ("batizado", "cargo")


# -------------------- OBREIROS --------------------
@admin.register(Obreiro)
class ObreiroAdmin(admin.ModelAdmin):
    list_display = ("nome", "cargo", "telefone", "email", "ativo")
    list_filter = ("ativo", "cargo")
    search_fields = ("nome", "cargo", "telefone", "email")


# -------------------- DEPARTAMENTOS --------------------
@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "ministerio")
    search_fields = ("nome",)


# -------------------- EVENTOS --------------------
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "data", "hora", "local", "categoria")
    list_filter = ("categoria", "data")
    search_fields = ("titulo", "descricao")
    # Removido prepopulated_fields pois 'slug' não existe mais


# -------------------- CONTRIBUIÇÕES --------------------
@admin.register(Contribuicao)
class ContribuicaoAdmin(admin.ModelAdmin):
    list_display = ("tipo", "valor", "data", "contribuinte", "identificacao")
    list_filter = ("tipo", "data")
    search_fields = ("contribuinte", "identificacao")


# -------------------- DESPESAS --------------------
@admin.register(Despesa)
class DespesaAdmin(admin.ModelAdmin):
    list_display = ("descricao", "valor", "data", "recibo")
    list_filter = ("data",)
    search_fields = ("descricao",)


# -------------------- MINISTÉRIO --------------------
@admin.register(Ministerio)
class MinisterioAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao", "responsavel", "data_criacao")
    search_fields = ("nome", "descricao", "responsavel")


# -------------------- VISITANTES --------------------
@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ("nome", "data_visita", "igreja_origem", "frequenta_igreja", "cristao")
    list_filter = ("frequenta_igreja", "cristao", "data_visita")
    search_fields = ("nome", "igreja_origem")


# -------------------- ESCALA DE SERVIÇO --------------------
@admin.register(EscalaServico)
class EscalaServicoAdmin(admin.ModelAdmin):
    list_display = ("data", "culto", "tarefa")
    list_filter = ("data",)
    filter_horizontal = ("obreiros",)
    search_fields = ("culto", "tarefa")


# -------------------- MISSÕES --------------------
@admin.register(Missao)
class MissaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "pais", "responsavel")
    search_fields = ("nome", "pais", "responsavel")


# -------------------- BANNERS --------------------
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("titulo", "ordem", "ativo")
    list_filter = ("ativo",)
    search_fields = ("titulo",)
