import uuid
from sqlmodel import SQLModel, Field
from pydantic import constr, validator

class Userbase(SQLModel):
    full_name: constr(strip_whitespace=True, min_length=1) = Field(default=None, max_length=50)
    username: constr(strip_whitespace=True, min_length=1) = Field(unique=True, max_length=20, index=True)
    email: str = Field(unique=True, max_length=50, index=True)
    

    @validator("email")
    def validator_email(cls, v):
        if " " in v:
            raise ValueError("Email tidak boleh mengandung spasi")
        return v


class UserCreate(Userbase):
    password: constr(min_length=8)


class UserOut(SQLModel):
    id: uuid.UUID
    full_name: constr(strip_whitespace=True, min_length=1) = Field(default=None, max_length=50)
    username: constr(strip_whitespace=True, min_length=1) = Field(max_length=20, index=True)
    email: str = Field(max_length=50, index=True)


class UserPublic(Userbase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int

class User(Userbase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    hash_password: str


class Token(SQLModel):
    access_token: str
    token_type: str = "Bearer"


class TokenPayload(SQLModel):
    sub: int | None = None