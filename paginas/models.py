from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class Usuario(AbstractUser):

    class TipoUsuario(models.TextChoices):
        TUTOR = 'TUTOR', 'Tutor'
        CUIDADOR = 'CUIDADOR', 'Cuidador'

    telefone = models.CharField(max_length=11)

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TipoUsuario.choices
    )

    data_criacao = models.DateTimeField(auto_now_add=True)

    # Tipo "AbstractUser" já define por padrão campos "first_name", "last_name", "password" e "email"
    # Para manter a coerência de campos em português, eles são renomeados abaixo

    @property
    def nome(self):
        return self.first_name

    @nome.setter
    def nome(self, value):
        self.first_name = value

    def set_senha(self, raw_password):
        self.set_password(raw_password)

    def verificar_senha(self, raw_password):
        return self.check_password(raw_password)

    def __str__(self):
        return self.nome or self.username


class Cuidador(models.Model):

    class UF(models.TextChoices):
        AC = 'AC', 'Acre'
        AL = 'AL', 'Alagoas'
        AP = 'AP', 'Amapá'
        AM = 'AM', 'Amazonas'
        BA = 'BA', 'Bahia'
        CE = 'CE', 'Ceará'
        DF = 'DF', 'Distrito Federal'
        ES = 'ES', 'Espírito Santo'
        GO = 'GO', 'Goiás'
        MA = 'MA', 'Maranhão'
        MT = 'MT', 'Mato Grosso'
        MS = 'MS', 'Mato Grosso do Sul'
        MG = 'MG', 'Minas Gerais'
        PA = 'PA', 'Pará'
        PB = 'PB', 'Paraíba'
        PR = 'PR', 'Paraná'
        PE = 'PE', 'Pernambuco'
        PI = 'PI', 'Piauí'
        RJ = 'RJ', 'Rio de Janeiro'
        RN = 'RN', 'Rio Grande do Norte'
        RS = 'RS', 'Rio Grande do Sul'
        RO = 'RO', 'Rondônia'
        RR = 'RR', 'Roraima'
        SC = 'SC', 'Santa Catarina'
        SP = 'SP', 'São Paulo'
        SE = 'SE', 'Sergipe'
        TO = 'TO', 'Tocantins'

    usuario = models.OneToOneField(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='cuidador'
    )

    servicos = models.ManyToManyField(
        'Servico',
        related_name='cuidadores'
    )

    descricao = models.CharField(max_length=250, null=False, blank=False)
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    cidade = models.CharField(max_length=50, null=False, blank=False)
    uf = models.CharField(max_length=2, choices=UF.choices, null=False, blank=False)

    def __str__(self):
        return f"Cuidador: {self.usuario.nome or self.usuario.username}"
    

class Pet(models.Model):

    class Especie(models.TextChoices):
        CACHORRO = 'CACHORRO', 'Cachorro'
        GATO = 'GATO', 'Gato'

    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='pets'
    )

    nome = models.CharField(max_length=150, null=False, blank=False)
    especie = models.CharField(max_length=20, choices=Especie.choices, null=False, blank=False)
    raca = models.CharField(max_length=150, null=False, blank=False)
    data_nascimento = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"{self.nome} ({self.get_especie_display()}) - {self.usuario.nome}"


class Disponibilidade(models.Model):

    cuidador = models.ForeignKey(
        'Cuidador',
        on_delete=models.CASCADE,
        related_name="disponibilidades"
    )

    data_inicio = models.DateTimeField(null=False, blank=False)
    data_fim = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return (
            f"{self.cuidador.usuario.nome} | "
            f"{self.data_inicio.strftime('%d/%m/%Y %H:%M')} "
            f"até {self.data_fim.strftime('%d/%m/%Y %H:%M')}"
        )


class Servico(models.Model):
    descricao = models.CharField(max_length=50, unique=True, null=False, blank=False)

    def __str__(self):
        return self.descricao

class Agendamento(models.Model):

    class FormaPagamento(models.TextChoices):
        PIX = 'PIX', 'Pix'
        CARTAO = 'CARTAO', 'Cartão'
        DINHEIRO = 'DINHEIRO', 'Dinheiro'

    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    cuidador = models.ForeignKey(
        'Cuidador',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    pet = models.ForeignKey(
        'Pet',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )

    forma_pagamento = models.CharField(max_length=20, choices=FormaPagamento.choices, null=False, blank=False)
    data_inicio = models.DateTimeField(null=False, blank=False)
    data_fim = models.DateTimeField(null=False, blank=False)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.usuario.nome} → {self.cuidador.usuario.nome} | "
            f"{self.pet.nome}"
        )


class Avaliacao(models.Model):
    agendamento = models.OneToOneField(
        'Agendamento',
        on_delete=models.CASCADE,
        related_name='avaliacao'
    )

    nota = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(max_length=250, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Avaliação {self.nota}/5 - "
            f"{self.agendamento.cuidador.usuario.nome}"
        )