from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from core.models import AnotacaoAdmin, ConfigPortal, Evento, PedidoOracao


class PublicPagesTests(TestCase):
    def test_index_page_returns_200(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_eventos_excludes_past_events(self):
        Evento.objects.create(titulo="Evento passado", data=date.today() - timedelta(days=1))
        Evento.objects.create(titulo="Evento futuro", data=date.today() + timedelta(days=2))

        response = self.client.get(reverse("eventos"))
        self.assertEqual(response.status_code, 200)

        eventos = list(response.context["eventos"])
        self.assertEqual(len(eventos), 1)
        self.assertEqual(eventos[0].titulo, "Evento futuro")

    def test_cultos_and_missoes_are_public(self):
        cultos_response = self.client.get(reverse("cultos"))
        missoes_response = self.client.get(reverse("missoes"))
        self.assertEqual(cultos_response.status_code, 200)
        self.assertEqual(missoes_response.status_code, 200)

    def test_pedido_oracao_creates_record(self):
        response = self.client.post(
            reverse("pedido_oracao"),
            {
                "nome": "Irmã Maria",
                "telefone": "21999999999",
                "email": "maria@example.com",
                "pedido": "Pedido especial de oração pela família.",
                "confidencial": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PedidoOracao.objects.count(), 1)
        pedido = PedidoOracao.objects.first()
        self.assertEqual(pedido.status, PedidoOracao.Status.PENDENTE)

    def test_pedido_oracao_redirects_to_whatsapp_when_number_is_configured(self):
        ConfigPortal.objects.create(
            nome_igreja="Igreja Teste",
            whatsapp_pedidos_oracao="+55 (21) 98888-7777",
        )
        response = self.client.post(
            reverse("pedido_oracao"),
            {
                "nome": "João",
                "telefone": "21911112222",
                "email": "joao@example.com",
                "pedido": "Preciso de oração por saúde.",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("https://wa.me/5521988887777?text="))
        self.assertEqual(PedidoOracao.objects.count(), 1)


class AuthAndPermissionsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="usuario",
            email="usuario@example.com",
            password="senha-forte-123",
        )
        self.superuser = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="senha-super-123",
        )

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_bloco_notas_requires_login(self):
        AnotacaoAdmin.objects.create(texto="Anotacao privada")
        response = self.client.get(reverse("bloco_notas"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_financeiro_redirects_non_superuser(self):
        self.client.login(username="usuario", password="senha-forte-123")
        response = self.client.get(reverse("financeiro"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_financeiro_allows_superuser(self):
        self.client.login(username="admin", password="senha-super-123")
        response = self.client.get(reverse("financeiro"))
        self.assertEqual(response.status_code, 200)
