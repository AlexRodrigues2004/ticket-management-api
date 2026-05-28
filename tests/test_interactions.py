import pytest
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import UserFactory, TicketFactory


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
class TestInteractions:
    def test_criar_interacao_em_chamado(self):
        user = UserFactory()
        ticket = TicketFactory(created_by=user)
        client = auth_client(user)

        response = client.post(f'/api/tickets/{ticket.pk}/interactions/', {
            'message': 'Preciso de mais informações.'
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_listar_interacoes_de_chamado(self):
        user = UserFactory()
        ticket = TicketFactory(created_by=user)
        client = auth_client(user)

        client.post(f'/api/tickets/{ticket.pk}/interactions/', {'message': 'Msg 1'})
        client.post(f'/api/tickets/{ticket.pk}/interactions/', {'message': 'Msg 2'})

        response = client.get(f'/api/tickets/{ticket.pk}/interactions/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

    def test_usuario_nao_autenticado_nao_pode_interagir(self):
        ticket = TicketFactory()
        client = APIClient()

        response = client.post(f'/api/tickets/{ticket.pk}/interactions/', {
            'message': 'Tentativa sem auth'
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
