from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: str


class UserList(BaseModel):
    user: list[UserPublic]
