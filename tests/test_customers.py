import pytest
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import UserFactory, AttendantFactory, AdminFactory, CustomerFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_client(api_client):
    user = AdminFactory()
    response = api_client.post('/api/auth/login/', {
        'username': user.username,
        'password': 'senha123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def attendant_client(api_client):
    user = AttendantFactory()
    response = api_client.post('/api/auth/login/', {
        'username': user.username,
        'password': 'senha123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def client_user_client(api_client):
    user = UserFactory()
    response = api_client.post('/api/auth/login/', {
        'username': user.username,
        'password': 'senha123'
    })
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.mark.django_db
class TestCustomerCreate:
    def test_attendant_pode_criar_cliente(self, attendant_client):
        payload = {
            'name': 'João Silva',
            'email': 'joao@teste.com',
            'phone': '11999999999'
        }
        response = attendant_client.post('/api/customers/', payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'João Silva'

    def test_cliente_nao_pode_criar_cliente(self, client_user_client):
        payload = {
            'name': 'Teste',
            'email': 'teste@teste.com',
            'phone': '11999999999'
        }
        response = client_user_client.post('/api/customers/', payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_email_duplicado_retorna_erro(self, attendant_client):
        CustomerFactory(email='duplicado@teste.com')
        payload = {
            'name': 'Outro',
            'email': 'duplicado@teste.com',
            'phone': '11999999999'
        }
        response = attendant_client.post('/api/customers/', payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCustomerList:
    def test_listar_clientes_autenticado(self, attendant_client):
        CustomerFactory.create_batch(3)
        response = attendant_client.get('/api/customers/')
        assert response.status_code == status.HTTP_200_OK

    def test_listar_clientes_sem_autenticacao(self, api_client):
        response = api_client.get('/api/customers/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestCustomerDelete:
    def test_admin_pode_deletar(self, admin_client):
        customer = CustomerFactory()
        response = admin_client.delete(f'/api/customers/{customer.pk}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_atendente_nao_pode_deletar(self, attendant_client):
        customer = CustomerFactory()
        response = attendant_client.delete(f'/api/customers/{customer.pk}/')
        assert response.status_code == status.HTTP_403_FORBIDDEN