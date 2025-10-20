from django.db import models

class ConfigPortal(models.Model):
    nome_igreja = models.CharField(max_length=200, default="Assembleia de Deus Só Jesus Salva")
    pastor = models.CharField(max_length=200, default="Pastora Angélica Coutinho dos Santos")
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    mensagem_boas_vindas = models.CharField(max_length=255, default="Seja bem-vindo(a) ao nosso portal!")
    imagem_fundo = models.ImageField(upload_to="fundos/", blank=True, null=True)

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

    def __str__(self):
        return self.titulo

class Contribuicao(models.Model):
    TIPO_CHOICES = [("Dízimo", "Dízimo"), ("Oferta", "Oferta"), ("Outros", "Outros")]
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    contribuinte = models.CharField("Nome do Contribuinte", max_length=150, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Contribuições"

    def __str__(self):
        return f"{self.tipo} - R$ {self.valor} ({self.contribuinte or 'Anônimo'})"

class Despesa(models.Model):
    descricao = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    class Meta:
        verbose_name_plural = "Despesas"

    def __str__(self):
        return f"{self.descricao} - R$ {self.valor}"

class Missao(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Missões"

    def __str__(self):
        return self.nome

class Visitante(models.Model):
    nome = models.CharField(max_length=100)
    data_visita = models.DateField()

    class Meta:
        verbose_name_plural = "Visitantes"

    def __str__(self):
        return self.nome

class ReuniaoMinisterial(models.Model):
    titulo = models.CharField(max_length=100)
    data = models.DateField()
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Reuniões Ministeriais"

    def __str__(self):
        return self.titulo
