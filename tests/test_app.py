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


def test_get_root_must_return_ok_and_message(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World!'}


def test_create_user_with_same_username_must_return_confliction(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'test',
            'email': 'luiz@gmail.com',
            'password': 'lhetoroelhefuro',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username already exists',
    }


def test_create_user_with_same_email_must_return_confliction(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'test65',
            'email': 'test@test.com',
            'password': 'lhetoroelhefuro',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Email already exists',
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'ruan carlos',
            'email': 'andrezitos@youtube.com',
            'password': 'passaro',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'ruan carlos',
        'id': user.id,
        'email': 'andrezitos@youtube.com',
    }


# def test_update_user_must_return_404(client, user, token):
#     response = client.put(
#         '/users/2',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'username': 'baesse',
#             'email': 'baesse@gmail.com',
#             'password': 'lula meu herói',
#         },
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@alice.com',
            'password': 'secret',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'alice',
            'email': 'alice@alice.com',
            'password': 'secret',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# def test_delete_user_must_return_404(client, user):
#     response = client.delete('/users/2')
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
