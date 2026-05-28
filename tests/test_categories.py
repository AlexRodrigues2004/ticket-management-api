import pytest
from rest_framework.test import APIClient
from rest_framework import status
from tests.factories import UserFactory, AttendantFactory, CategoryFactory


@pytest.fixture
def api_client():
    return APIClient()


def get_token(api_client, user):
    response = api_client.post('/api/auth/login/', {
        'username': user.username,
        'password': 'senha123'
    })
    return response.data['access']


@pytest.mark.django_db
class TestCategoryCreate:
    def test_atendente_pode_criar_categoria(self):
        client = APIClient()
        user = AttendantFactory()
        token = get_token(client, user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = client.post('/api/categories/', {
            'name': 'Suporte Técnico',
            'description': 'Problemas técnicos gerais'
        })
        assert response.status_code == status.HTTP_201_CREATED

    def test_cliente_nao_pode_criar_categoria(self):
        client = APIClient()
        user = UserFactory()
        token = get_token(client, user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = client.post('/api/categories/', {'name': 'Teste'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_nome_duplicado_retorna_erro(self):
        client = APIClient()
        user = AttendantFactory()
        token = get_token(client, user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        CategoryFactory(name='Categoria Única')

        response = client.post('/api/categories/', {'name': 'Categoria Única'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestCategoryList:
    def test_listar_categorias(self):
        client = APIClient()
        user = UserFactory()
        token = get_token(client, user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        CategoryFactory.create_batch(3)

        response = client.get('/api/categories/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3
