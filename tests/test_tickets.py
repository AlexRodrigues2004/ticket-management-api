import pytest
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import (
    UserFactory, AttendantFactory,
    CustomerFactory, CategoryFactory, TicketFactory
)


@pytest.fixture
def api_client():
    return APIClient()


def auth_client(user):
    client = APIClient()
    response = client.post('/api/auth/login/', {
        'username': user.username,
        'password': 'senha123'
    })
    token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.mark.django_db
class TestTicketCreate:
    def test_usuario_autenticado_pode_criar_chamado(self):
        user = UserFactory()
        customer = CustomerFactory()
        category = CategoryFactory()
        client = auth_client(user)

        payload = {
            'title': 'Erro no sistema',
            'description': 'Sistema não abre',
            'customer': customer.pk,
            'category': category.pk,
            'priority': 'alta'
        }
        response = client.post('/api/tickets/', payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Erro no sistema'

    def test_usuario_nao_autenticado_nao_pode_criar(self, api_client):
        response = api_client.post('/api/tickets/', {})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTicketPermissions:
    def test_cliente_ve_apenas_proprios_chamados(self):
        user1 = UserFactory()
        user2 = UserFactory()
        TicketFactory(created_by=user1)
        TicketFactory(created_by=user2)

        client = auth_client(user1)
        response = client.get('/api/tickets/')
        assert response.status_code == status.HTTP_200_OK
        for ticket in response.data:
            assert ticket['created_by'] == user1.pk

    def test_atendente_ve_todos_os_chamados(self):
        user1 = UserFactory()
        user2 = UserFactory()
        TicketFactory(created_by=user1)
        TicketFactory(created_by=user2)

        attendant = AttendantFactory()
        client = auth_client(attendant)
        response = client.get('/api/tickets/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2


@pytest.mark.django_db
class TestTicketStatus:
    def test_atendente_pode_alterar_status(self):
        ticket = TicketFactory()
        attendant = AttendantFactory()
        client = auth_client(attendant)

        response = client.patch(f'/api/tickets/{ticket.pk}/status/', {
            'status': 'em_atendimento'
        })
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'em_atendimento'

    def test_cliente_nao_pode_alterar_status(self):
        user = UserFactory()
        ticket = TicketFactory(created_by=user)
        client = auth_client(user)

        response = client.patch(f'/api/tickets/{ticket.pk}/status/', {
            'status': 'resolvido'
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestTicketFilters:
    def test_filtrar_por_status(self):
        attendant = AttendantFactory()
        TicketFactory(status='aberto')
        TicketFactory(status='resolvido')

        client = auth_client(attendant)
        response = client.get('/api/tickets/?status=aberto')
        assert response.status_code == status.HTTP_200_OK
        for ticket in response.data:
            assert ticket['status'] == 'aberto'

    def test_busca_por_titulo(self):
        attendant = AttendantFactory()
        TicketFactory(title='Problema no login')
        TicketFactory(title='Outro assunto')

        client = auth_client(attendant)
        response = client.get('/api/tickets/?search=login')
        assert response.status_code == status.HTTP_200_OK
        assert any('login' in t['title'].lower() for t in response.data)
