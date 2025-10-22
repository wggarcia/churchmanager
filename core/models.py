# core/models.py
from django.db import models

class ConfigPortal(models.Model):
    nome_igreja = models.CharField(max_length=200)
    pastor = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    mensagem_boas_vindas = models.CharField(max_length=255, default="Seja bem-vindo(a) ao nosso portal!")
    imagem_fundo = models.ImageField(upload_to="fundos/", blank=True, null=True)
    banner = models.ImageField(upload_to="banners/", blank=True, null=True)
    banner_titulo = models.CharField(max_length=150, blank=True, default="")
    banner_subtitulo = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        verbose_name = "⚙️ Configuração do Sistema"
        verbose_name_plural = "⚙️ Configurações do Sistema"

    def __str__(self):
        return self.nome_igreja


class Membro(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    batizado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Membros"

    def __str__(self):
        return self.nome


class Ministerio(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Ministérios"

    def __str__(self):
        return self.nome


class Departamento(models.Model):
    nome = models.CharField(max_length=100)
    ministerio = models.ForeignKey(Ministerio, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return f"{self.nome} ({self.ministerio})"


class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data = models.DateField()

    class Meta:
        verbose_name_plural = "Eventos"
        ordering = ["-data"]

    def __str__(self):
        return self.titulo


TIPOS_CONTRIB = (("Dízimo", "Dízimo"), ("Oferta", "Oferta"), ("Outros", "Outros"))

class Contribuicao(models.Model):
    tipo = models.CharField(max_length=50, choices=TIPOS_CONTRIB)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    contribuinte = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nome do Contribuinte")
    outros_destino = models.CharField(max_length=200, blank=True, default="", help_text="Destino/descrição para 'Outros'.")

    class Meta:
        verbose_name_plural = "Contribuições"

    def __str__(self):
        extra = f" ({self.contribuinte})" if self.contribuinte else ""
        return f"{self.tipo} - R$ {self.valor:.2f}{extra}"


class Despesa(models.Model):
    descricao = models.CharField(max_length=120)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    recibo = models.FileField(upload_to="recibos/", blank=True, null=True)  # vai para GCS se configurado

    class Meta:
        verbose_name_plural = "Despesas"

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor:.2f}"


class Missao(models.Model):
    nome = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = "Missões"

    def __str__(self):
        return self.nome


class Visitante(models.Model):
    nome = models.CharField(max_length=120)
    data_visita = models.DateField()
    frequenta_igreja = models.BooleanField(default=False)
    igreja_origem = models.CharField(max_length=150, blank=True, default="")
    telefone = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Visitantes"
        ordering = ["-data_visita"]

    def __str__(self):
        return self.nome


CARGOS = (
    ("Diácono", "Diácono"),
    ("Presbítero", "Presbítero"),
    ("Cooperador", "Cooperador"),
    ("Evangelista", "Evangelista"),
    ("Pastor", "Pastor"),
)

class Obreiro(models.Model):
    nome = models.CharField(max_length=120)
    cargo = models.CharField(max_length=30, choices=CARGOS)
    telefone = models.CharField(max_length=20, blank=True, default="")
    email = models.EmailField(blank=True, default="")

    class Meta:
        verbose_name_plural = "Obreiros"

    def __str__(self):
        return f"{self.nome} ({self.cargo})"


class EscalaServico(models.Model):
    data = models.DateField()
    culto = models.CharField(max_length=120, help_text="Ex.: Culto de Doutrina, EBD, Santa Ceia…")
    obreiros = models.ManyToManyField(Obreiro, blank=True)

    class Meta:
        verbose_name = "Escala de Serviço"
        verbose_name_plural = "Escalas de Serviço"
        ordering = ["-data"]

    def __str__(self):
        return f"{self.culto} - {self.data:%d/%m/%Y}"
