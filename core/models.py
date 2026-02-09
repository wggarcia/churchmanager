from django.db import models
from django.utils import timezone

# -------------------- CONFIGURAÇÃO DO PORTAL --------------------
class ConfigPortal(models.Model):
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
