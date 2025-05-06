from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from sqlalchemy.testing.pickleable import User

from fast_zero.db import session
from fast_zero.schemas import UserList, UserPublic, UserSchema

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Hello World!'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    session.add(user)
    session.commit()
    return user


@app.get('/users', response_model=UserList)
def read_users():
    return {'users': session.query(User).all()}


@app.get('/users/{user_id}', response_model=UserPublic)
def read_user(user_id: int):
    user = session.query(User).get(user_id).first()
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    db_user = session.query(User).get(user_id).first()
    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user = user
    session.add(db_user)
    session.commit()

    return db_user


@app.delete('/users/{user_id}')
def delete_user(user_id: int):
    db_user = session.query(User).get(user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted'}
