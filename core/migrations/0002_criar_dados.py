from django.db import migrations
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from datetime import datetime


def criar_dados(apps, schema_editor):
    Usuario = apps.get_model('core', 'Usuario')
    Cuidador = apps.get_model('core', 'Cuidador')
    Servico = apps.get_model('core', 'Servico')
    Disponibilidade = apps.get_model('core', 'Disponibilidade')
    Agendamento = apps.get_model('core', 'Agendamento')
    Avaliacao = apps.get_model('core', 'Avaliacao')

    # Criar serviços
    hospedagem = Servico.objects.create(descricao="Hospedagem")
    passeio = Servico.objects.create(descricao="Passeio")
    visita = Servico.objects.create(descricao="Visita")
    daycare = Servico.objects.create(descricao="Day Care")

    # Criar usuário cuidador
    user_cuidador = Usuario.objects.create(
        username="joao",
        first_name="João",
        email="joao@email.com",
        password=make_password("123456"),
        tipo_usuario="CUIDADOR",
    )

    cuidador = Cuidador.objects.create(
        usuario=user_cuidador,
        descricao="Cuido com muito carinho",
        valor_diaria=Decimal("80.00"),
        cidade="São Paulo",
        uf="SP"
    )

    cuidador.servicos.add(hospedagem, passeio, visita, daycare)

    # Disponibilidade
    Disponibilidade.objects.create(
        cuidador=cuidador,
        data_inicio=datetime(2026, 3, 1, 8, 0),
        data_fim=datetime(2026, 3, 30, 18, 0),
    )

    # Criar tutor
    tutor = Usuario.objects.create(
        username="augusto",
        first_name="Augusto",
        email="augusto@email.com",
        password=make_password("123456"),
        tipo_usuario="TUTOR",
    )

    # Criar pet
    Pet = apps.get_model('core', 'Pet')
    pet = Pet.objects.create(
        usuario=tutor,
        nome="Rex",
        especie="CACHORRO",
        raca="Labrador",
        data_nascimento=datetime(2020, 5, 10),
    )

    # Criar agendamento
    agendamento = Agendamento.objects.create(
        usuario=tutor,
        cuidador=cuidador,
        pet=pet,
        forma_pagamento="PIX",
        data_inicio=datetime(2026, 3, 5, 9, 0),
        data_fim=datetime(2026, 3, 7, 18, 0),
        valor_total=Decimal("160.00"),
    )

    # Avaliação
    Avaliacao.objects.create(
        agendamento=agendamento,
        nota=5,
        comentario="Excelente atendimento!"
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_dados),
    ]