from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.json() == {'users': [user_schema]}


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@alice.com',
            'password': 'secret',
        },
    )

    client.put(
        f'/users/{user.id}',
        json={
            'username': 'alice',
            'password': 'alicia@gmail.com',
            'password2': '<PASSWORD>',
        },
    )
