from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import func, select
from typing import Any, Annotated

from api.deps import SessionDep, CurrentUser
from handlers.users import register_user, get_user_by_email_or_username, authentication
from models.users import UserCreate, UserOut, UsersOut, User, Token, UserPublic
from security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()

@router.get("/", response_model=UsersOut)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    count_statement = select(func.count()).select_from(User)
    count = await session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = await session.exec(statement).all()

    return UsersOut(data=users, count=count)


@router.post("/register", response_model=UserOut)
async def register(*, session: SessionDep, user_in: UserCreate) -> Any:
    user = await get_user_by_email_or_username(session=session, email=user_in.email, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email or username already exists in the system."
        )
    user = await register_user(session=session, user_create=user_in)
    return user


@router.post("/login/access-token")
async def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await authentication(
        session=session, email_or_username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )



@router.post("/login/test-token", response_model=UserPublic)
async def login_test_token(current_user: CurrentUser):
    """untuk meanmpilak user"""
    return current_user
