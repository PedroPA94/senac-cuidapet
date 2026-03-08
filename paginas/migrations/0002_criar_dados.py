from django.db import migrations
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from datetime import datetime


def criar_dados(apps, schema_editor):
    Usuario = apps.get_model('paginas', 'Usuario')
    Cuidador = apps.get_model('paginas', 'Cuidador')
    Servico = apps.get_model('paginas', 'Servico')
    Disponibilidade = apps.get_model('paginas', 'Disponibilidade')
    Agendamento = apps.get_model('paginas', 'Agendamento')
    Avaliacao = apps.get_model('paginas', 'Avaliacao')

    # Criar serviços
    hospedagem = Servico.objects.create(descricao="Hospedagem")
    passeio = Servico.objects.create(descricao="Passeio")
    visita = Servico.objects.create(descricao="Visita")
    daycare = Servico.objects.create(descricao="Day Care")

    # Criar cuidadores
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
        uf="SP",
    )

    cuidador.servicos.add(hospedagem, passeio, visita, daycare)

    Disponibilidade.objects.create(
        cuidador=cuidador,
        data_inicio=datetime(2026, 3, 1, 8, 0),
        data_fim=datetime(2026, 3, 30, 18, 0),
    )

    user_cuidador2 = Usuario.objects.create(
        username="maria",
        first_name="Maria",
        email="maria@email.com",
        password=make_password("123456"),
        tipo_usuario="CUIDADOR",
    )

    cuidador2 = Cuidador.objects.create(
        usuario=user_cuidador2,
        descricao="Amo cuidar de pets e brincar com eles.",
        valor_diaria=Decimal("90.00"),
        cidade="Rio de Janeiro",
        uf="RJ",
    )
    cuidador2.servicos.add(hospedagem, passeio, visita)
    Disponibilidade.objects.create(
        cuidador=cuidador2,
        data_inicio=datetime(2026, 3, 5, 9, 0),
        data_fim=datetime(2026, 3, 25, 19, 0),
    )

    user_cuidador3 = Usuario.objects.create(
        username="carlos",
        first_name="Carlos",
        email="carlos@email.com",
        password=make_password("123456"),
        tipo_usuario="CUIDADOR",
    )

    cuidador3 = Cuidador.objects.create(
        usuario=user_cuidador3,
        descricao="Experiência com cães e gatos de todas as idades.",
        valor_diaria=Decimal("75.00"),
        cidade="Belo Horizonte",
        uf="MG",
    )
    cuidador3.servicos.add(hospedagem, daycare)
    Disponibilidade.objects.create(
        cuidador=cuidador3,
        data_inicio=datetime(2026, 3, 2, 7, 0),
        data_fim=datetime(2026, 3, 28, 20, 0),
    )

    user_cuidador4 = Usuario.objects.create(
        username="ana",
        first_name="Ana",
        email="ana@email.com",
        password=make_password("123456"),
        tipo_usuario="CUIDADOR",
    )

    cuidador4 = Cuidador.objects.create(
        usuario=user_cuidador4,
        descricao="Cuidando com paciência e atenção aos detalhes.",
        valor_diaria=Decimal("85.00"),
        cidade="Curitiba",
        uf="PR",
    )
    cuidador4.servicos.add(passeio, visita)
    Disponibilidade.objects.create(
        cuidador=cuidador4,
        data_inicio=datetime(2026, 3, 3, 8, 30),
        data_fim=datetime(2026, 3, 29, 18, 30),
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
    Pet = apps.get_model('paginas', 'Pet')
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
        ('paginas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(criar_dados),
    ]