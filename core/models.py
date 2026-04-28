from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# -------------------- CONFIGURAÇÃO DO PORTAL --------------------
class ConfigPortal(models.Model):
    nome_sistema = models.CharField(
        "Nome do Sistema",
        max_length=120,
        default="ChurchManager Pro",
        help_text="Nome comercial exibido no painel e no login.",
    )
    slogan_sistema = models.CharField(
        "Slogan do Sistema",
        max_length=180,
        blank=True,
        null=True,
        default="Gestão inteligente para igrejas",
    )
    nome_igreja = models.CharField(
        "Nome da Igreja",
        max_length=150,
        default="Assembleia de Deus Só Jesus Salva",
    )
    pastor = models.CharField(
        "Pastor Responsável",
        max_length=100,
        blank=True,
        null=True,
        default="Pastora Angélica Coutinho dos Santos",
    )
    mensagem_boas_vindas = models.TextField(
        "Mensagem de boas-vindas",
        blank=True,
        null=True,
        help_text="Texto exibido na página inicial do portal.",
    )
    chave_igreja = models.SlugField(
        "Chave da Igreja",
        max_length=80,
        blank=True,
        null=True,
        unique=True,
        help_text="Identificador único para versões white-label (ex: igreja-central).",
    )
    dominio_oficial = models.CharField(
        "Domínio Oficial",
        max_length=120,
        blank=True,
        null=True,
        help_text="Ex: adsjs.com.br",
    )
    cidade = models.CharField("Cidade", max_length=80, blank=True, null=True)
    estado = models.CharField("Estado", max_length=40, blank=True, null=True)
    telefone_contato = models.CharField("Telefone de Contato", max_length=25, blank=True, null=True)
    email_contato = models.EmailField("E-mail de Contato", blank=True, null=True)
    instagram_url = models.URLField("Instagram", blank=True, null=True)
    youtube_url = models.URLField("YouTube", blank=True, null=True)
    facebook_url = models.URLField("Facebook", blank=True, null=True)
    recebe_novas_igrejas = models.BooleanField(
        "Instância comercial (revenda ativa)",
        default=True,
        help_text="Marque para sinalizar esta instalação como pronta para vender para outras igrejas.",
    )

    cor_primaria = models.CharField(
        "Cor Primária",
        max_length=7,
        default="#0f4c81",
        validators=[RegexValidator(regex=r"^#[0-9A-Fa-f]{6}$", message="Use formato hexadecimal, ex: #0f4c81")],
    )
    cor_secundaria = models.CharField(
        "Cor Secundária",
        max_length=7,
        default="#1f7a8c",
        validators=[RegexValidator(regex=r"^#[0-9A-Fa-f]{6}$", message="Use formato hexadecimal, ex: #1f7a8c")],
    )
    cor_destaque = models.CharField(
        "Cor de Destaque",
        max_length=7,
        default="#f4b942",
        validators=[RegexValidator(regex=r"^#[0-9A-Fa-f]{6}$", message="Use formato hexadecimal, ex: #f4b942")],
    )
    cor_fundo = models.CharField(
        "Cor de Fundo",
        max_length=7,
        default="#f4f7fb",
        validators=[RegexValidator(regex=r"^#[0-9A-Fa-f]{6}$", message="Use formato hexadecimal, ex: #f4f7fb")],
    )

    logo = models.ImageField(
        "Logo da Igreja",
        upload_to="config/",
        blank=True,
        null=True,
    )
    plano_fundo = models.ImageField(
        "Plano de Fundo",
        upload_to="config/",
        blank=True,
        null=True,
        help_text="Imagem usada como plano de fundo do site.",
    )

    atualizado_em = models.DateTimeField("Última atualização", auto_now=True)

    class Meta:
        verbose_name = "Configuração do Portal"
        verbose_name_plural = "Configurações do Portal"

    def __str__(self):
        return self.nome_igreja or "Configuração do Portal"


# -------------------- BANNERS --------------------
class Banner(models.Model):
    titulo = models.CharField(max_length=100, blank=True, null=True)
    subtitulo = models.CharField(max_length=200, blank=True, null=True)
    imagem = models.ImageField(upload_to="banners/")
    ordem = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ["ordem"]
        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        return self.titulo or f"Banner {self.id}"


# -------------------- MEMBROS --------------------
class Membro(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    batizado = models.BooleanField(default=False)
    cargo = models.CharField(max_length=100, blank=True, null=True)
    data_cadastro = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

    def __str__(self):
        return self.nome


# -------------------- OBREIROS --------------------
class Obreiro(models.Model):
    nome = models.CharField("Nome do obreiro", max_length=100)
    cargo = models.CharField("Cargo/Função", max_length=100, blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    ativo = models.BooleanField("Ativo", default=True)
    data_cadastro = models.DateField("Data de cadastro", auto_now_add=True)

    class Meta:
        verbose_name = "Obreiro"
        verbose_name_plural = "Obreiros"
        ordering = ["nome"]

    def __str__(self):
        return self.nome



# -------------------- EVENTOS --------------------
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data = models.DateField(default=timezone.now)
    hora = models.TimeField(blank=True, null=True)
    local = models.CharField(max_length=150, blank=True, null=True)
    capa = models.ImageField(upload_to="eventos/", blank=True, null=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    preco = models.CharField(max_length=30, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["-data"]

    def __str__(self):
        return self.titulo


# -------------------- CONTRIBUIÇÕES --------------------
class Contribuicao(models.Model):
    TIPO_CHOICES = [
        ("Dízimo", "Dízimo"),
        ("Oferta", "Oferta"),
        ("Outros", "Outros"),
    ]
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default="Dízimo")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    contribuinte = models.CharField(max_length=100, blank=True, null=True)
    identificacao = models.CharField(max_length=100, blank=True, null=True)
    data = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Contribuição"
        verbose_name_plural = "Contribuições"

    def __str__(self):
        return f"{self.tipo} - {self.valor}"


# -------------------- DESPESAS --------------------
class Despesa(models.Model):
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(default=timezone.now)
    recibo = models.FileField(upload_to="recibos/", blank=True, null=True)

    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"

    def __str__(self):
        return self.descricao


# -------------------- DEPARTAMENTOS --------------------
class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    ministerio = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nome


# -------------------- VISITANTES --------------------
class Visitante(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    data_visita = models.DateField(default=timezone.now)
    frequenta_igreja = models.BooleanField(default=False)
    cristao = models.BooleanField(default=False)
    igreja_origem = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"

    def __str__(self):
        return self.nome


# -------------------- MINISTÉRIO --------------------
class Ministerio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_criacao = models.DateField(default=timezone.now)
    responsavel = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Ministério"
        verbose_name_plural = "Ministérios"

    def __str__(self):
        return self.nome


# -------------------- MISSÕES --------------------
class Missao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    responsavel = models.CharField(max_length=100, blank=True, null=True)
    contato = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Missão"
        verbose_name_plural = "Missões"

    def __str__(self):
        return self.nome


# -------------------- PEDIDO DE ORAÇÃO --------------------
class PedidoOracao(models.Model):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        EM_ACOMPANHAMENTO = "EM_ACOMPANHAMENTO", "Em acompanhamento"
        CONCLUIDO = "CONCLUIDO", "Concluído"

    nome = models.CharField("Nome", max_length=120, blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=25, blank=True, null=True)
    email = models.EmailField("E-mail", blank=True, null=True)
    pedido = models.TextField("Pedido")
    confidencial = models.BooleanField("Confidencial", default=True)
    status = models.CharField(
        "Status",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Pedido de Oração"
        verbose_name_plural = "Pedidos de Oração"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Pedido de Oração - {self.nome or 'Anônimo'}"


# -------------------- ESCALA DE SERVIÇO --------------------
class EscalaServico(models.Model):
    culto = models.CharField("Culto", max_length=100, default="Culto de Domingo")
    data = models.DateField("Data do Culto", default=timezone.now)
    tarefa = models.CharField("Função / Tarefa", max_length=150, blank=True, null=True)
    local = models.CharField("Local do Culto", max_length=150, blank=True, null=True)
    obreiros = models.ManyToManyField(Obreiro, verbose_name="Obreiros Escalados", blank=True)
    observacoes = models.TextField("Observações", blank=True, null=True)

    class Meta:
        verbose_name = "Escala de Culto"
        verbose_name_plural = "Escala de Cultos"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.culto} - {self.data.strftime('%d/%m/%Y')}"


# 🔹 NOVO: Conecta Escala + Obreiro + Função (sem apagar nada seu)
class EscalaObreiro(models.Model):
    escala = models.ForeignKey(EscalaServico, on_delete=models.CASCADE)
    obreiro = models.ForeignKey(Obreiro, on_delete=models.CASCADE)
    funcao = models.CharField("Função no Culto", max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = "Obreiro na Escala"
        verbose_name_plural = "Obreiros nas Escalas"
        ordering = ["escala", "obreiro"]

    def __str__(self):
        return f"{self.obreiro.nome} - {self.funcao or 'Sem função'}"


# -------------------- BLOCO DE NOTAS --------------------
class Nota(models.Model):
    titulo = models.CharField(
        "Título",
        max_length=150,
        blank=True,
        null=True
    )
    conteudo = models.TextField(
        "Conteúdo da Nota"
    )
    criado_em = models.DateTimeField(
        "Criado em",
        auto_now_add=True
    )
    atualizado_em = models.DateTimeField(
        "Atualizado em",
        auto_now=True
    )

    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Bloco de Notas"
        ordering = ["-atualizado_em"]

    def __str__(self):
        return self.titulo or f"Nota {self.id}"

# -------------------- ANOTAÇÃO ADMINISTRATIVA --------------------
class AnotacaoAdmin(models.Model):
    titulo = models.CharField(
        "Título",
        max_length=150,
        default="Anotação Administrativa"
    )
    texto = models.TextField(
        "Anotação"
    )
    atualizado_em = models.DateTimeField(
        "Última atualização",
        auto_now=True
    )

    class Meta:
        verbose_name = "Anotação do Admin"
        verbose_name_plural = "Anotação do Admin"

    def __str__(self):
        return self.titulo
