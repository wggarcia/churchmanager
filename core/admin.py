from django.contrib import admin
from .models import (
    ConfigPortal,
    Banner,
    Membro,
    Obreiro,
    Departamento,
    Evento,
    Contribuicao,
    Despesa,
    Ministerio,
    Visitante,
    Missao,
    EscalaServico,
    EscalaObreiro,
    PedidoOracao,
    Nota,             # 👈 IMPORTA NOTA
    AnotacaoAdmin,    # 👈 IMPORTA ANOTAÇÃO
)

admin.site.site_header = "ChurchManager Pro Admin"
admin.site.site_title = "ChurchManager Pro"
admin.site.index_title = "Painel de Administração"


# -------------------- CONFIGURAÇÃO DO PORTAL --------------------
@admin.register(ConfigPortal)
class ConfigPortalAdmin(admin.ModelAdmin):
    list_display = ("nome_igreja", "nome_sistema", "dominio_oficial", "recebe_novas_igrejas", "atualizado_em")
    search_fields = ("nome_igreja", "nome_sistema", "pastor", "dominio_oficial", "chave_igreja")
    list_filter = ("recebe_novas_igrejas", "estado")
    fieldsets = (
        ("Produto / White-label", {
            "fields": (
                "nome_sistema",
                "slogan_sistema",
                "chave_igreja",
                "dominio_oficial",
                "recebe_novas_igrejas",
            ),
            "description": "Dados comerciais da instância para venda e personalização.",
        }),
        ("Informações da Igreja", {
            "fields": (
                "nome_igreja",
                "pastor",
                "mensagem_boas_vindas",
                "agenda_cultos",
                "cidade",
                "estado",
                "telefone_contato",
                "whatsapp_pedidos_oracao",
                "email_contato",
            ),
            "description": "Configurações gerais do portal."
        }),
        ("Redes sociais", {
            "fields": ("instagram_url", "youtube_url", "facebook_url"),
        }),
        ("Tema visual", {
            "fields": ("cor_primaria", "cor_secundaria", "cor_destaque", "cor_fundo"),
            "description": "Cores principais do portal (formato hexadecimal).",
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
# Novo bloco — inclui a relação entre obreiro e função no culto
class EscalaObreiroInline(admin.TabularInline):
    model = EscalaObreiro
    extra = 1  # adiciona 1 linha vazia por padrão

@admin.register(EscalaServico)
class EscalaServicoAdmin(admin.ModelAdmin):
    list_display = ("data", "culto", "local")
    list_filter = ("data",)
    search_fields = ("culto", "local")
    inlines = [EscalaObreiroInline]  # 👈 adiciona os obreiros e funções dentro da escala


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


@admin.register(PedidoOracao)
class PedidoOracaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "status", "confidencial", "telefone", "email", "criado_em")
    list_filter = ("status", "confidencial", "criado_em")
    search_fields = ("nome", "telefone", "email", "pedido")
    readonly_fields = ("criado_em", "atualizado_em")
    list_editable = ("status",)


@admin.register(AnotacaoAdmin)
class AnotacaoAdminAdmin(admin.ModelAdmin):
    list_display = ("titulo", "atualizado_em")
    search_fields = ("titulo", "conteudo")
    ordering = ("-atualizado_em",)
