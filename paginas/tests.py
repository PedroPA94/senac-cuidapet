from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Agendamento, Cuidador, Pet, Usuario


class LoginPerfilTests(TestCase):
    def setUp(self):
        self.tutor = Usuario.objects.create_user(
            username='login-tutor@email.com', password='senha-forte-123',
            first_name='Tutor', telefone='11999999999', tipo_usuario=Usuario.TipoUsuario.TUTOR,
        )
        self.cuidador = Usuario.objects.create_user(
            username='login-cuidador@email.com', password='senha-forte-123',
            first_name='Cuidador', telefone='11988888888', tipo_usuario=Usuario.TipoUsuario.CUIDADOR,
        )

    def test_tutor_entra_pela_opcao_tutor(self):
        response = self.client.post(reverse('login'), {
            'username': self.tutor.username, 'password': 'senha-forte-123', 'tipo_usuario': 'TUTOR',
        })
        self.assertRedirects(response, reverse('home'))

    def test_cuidador_entra_pela_opcao_cuidador(self):
        response = self.client.post(reverse('login'), {
            'username': self.cuidador.username, 'password': 'senha-forte-123', 'tipo_usuario': 'CUIDADOR',
        })
        self.assertRedirects(response, reverse('cuidador_solicitacoes'), fetch_redirect_response=False)

    def test_perfil_incorreto_nao_autentica(self):
        response = self.client.post(reverse('login'), {
            'username': self.tutor.username, 'password': 'senha-forte-123', 'tipo_usuario': 'CUIDADOR',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'Esta conta está cadastrada como tutor')

    def test_login_exige_selecao_de_perfil(self):
        response = self.client.post(reverse('login'), {
            'username': self.tutor.username, 'password': 'senha-forte-123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, 'Selecione se deseja entrar como tutor ou cuidador')


class CuidadorSolicitacoesTests(TestCase):
    def setUp(self):
        self.cuidador_user = Usuario.objects.create_user(username='cuidador-teste@email.com', password='senha-forte-123', first_name='Carla', telefone='11999999999', tipo_usuario=Usuario.TipoUsuario.CUIDADOR)
        self.outro_cuidador_user = Usuario.objects.create_user(username='outro-cuidador@email.com', password='senha-forte-123', first_name='Paulo', telefone='11988888888', tipo_usuario=Usuario.TipoUsuario.CUIDADOR)
        self.tutor = Usuario.objects.create_user(username='tutor-teste@email.com', password='senha-forte-123', first_name='Ana', telefone='11977777777', tipo_usuario=Usuario.TipoUsuario.TUTOR)
        self.cuidador = Cuidador.objects.create(usuario=self.cuidador_user, descricao='Cuidadora de teste', valor_diaria=Decimal('90.00'), cidade='São Paulo', uf='SP')
        self.outro_cuidador = Cuidador.objects.create(usuario=self.outro_cuidador_user, descricao='Outro cuidador', valor_diaria=Decimal('80.00'), cidade='Campinas', uf='SP')
        self.pet = Pet.objects.create(usuario=self.tutor, nome='Mel', especie=Pet.Especie.CACHORRO, raca='SRD', data_nascimento='2021-05-10')
        agora = timezone.now()
        self.agendamento = Agendamento.objects.create(usuario=self.tutor, cuidador=self.cuidador, pet=self.pet, forma_pagamento=Agendamento.FormaPagamento.PIX, data_inicio=agora + timedelta(days=2), data_fim=agora + timedelta(days=4), valor_total=Decimal('270.00'))

    def test_painel_exibe_apenas_solicitacoes_do_cuidador_logado(self):
        Agendamento.objects.create(usuario=self.tutor, cuidador=self.outro_cuidador, pet=self.pet, forma_pagamento=Agendamento.FormaPagamento.DINHEIRO, data_inicio=timezone.now() + timedelta(days=5), data_fim=timezone.now() + timedelta(days=6), valor_total=Decimal('160.00'))
        self.client.force_login(self.cuidador_user)
        response = self.client.get(reverse('cuidador_solicitacoes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cuidador_dashboard.html')
        self.assertContains(response, 'R$ 270,00')
        self.assertNotContains(response, 'R$ 160,00')

    def test_dashboard_soma_ganhos_apenas_de_servicos_concluidos(self):
        self.agendamento.status = Agendamento.Status.CONCLUIDO
        self.agendamento.save(update_fields=['status'])
        Agendamento.objects.create(
            usuario=self.tutor,
            cuidador=self.cuidador,
            pet=self.pet,
            forma_pagamento=Agendamento.FormaPagamento.PIX,
            status=Agendamento.Status.ACEITO,
            data_inicio=timezone.now() + timedelta(days=8),
            data_fim=timezone.now() + timedelta(days=9),
            valor_total=Decimal('900.00'),
        )
        self.client.force_login(self.cuidador_user)
        response = self.client.get(reverse('cuidador_solicitacoes'))
        self.assertEqual(response.context['total_ganhos'], Decimal('270.00'))
        self.assertContains(response, 'R$ 270,00')

    def test_cuidador_pode_aceitar_solicitacao_pendente(self):
        self.client.force_login(self.cuidador_user)
        response = self.client.post(reverse('cuidador_solicitacao_status', args=[self.agendamento.pk, 'aceitar']))
        self.assertRedirects(response, reverse('cuidador_solicitacao_detail', args=[self.agendamento.pk]))
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, Agendamento.Status.ACEITO)

    def test_cuidador_pode_recusar_solicitacao_pendente(self):
        self.client.force_login(self.cuidador_user)
        self.client.post(reverse('cuidador_solicitacao_status', args=[self.agendamento.pk, 'recusar']))
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, Agendamento.Status.RECUSADO)

    def test_decisao_nao_pode_ser_alterada(self):
        self.agendamento.status = Agendamento.Status.ACEITO
        self.agendamento.save(update_fields=['status'])
        self.client.force_login(self.cuidador_user)
        self.client.post(reverse('cuidador_solicitacao_status', args=[self.agendamento.pk, 'recusar']))
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, Agendamento.Status.ACEITO)

    def test_cuidador_nao_acessa_solicitacao_de_outro_cuidador(self):
        self.client.force_login(self.outro_cuidador_user)
        response = self.client.get(reverse('cuidador_solicitacao_detail', args=[self.agendamento.pk]))
        self.assertEqual(response.status_code, 404)

    def test_tutor_nao_acessa_area_do_cuidador(self):
        self.client.force_login(self.tutor)
        response = self.client.get(reverse('cuidador_solicitacoes'))
        self.assertRedirects(response, reverse('home'))
