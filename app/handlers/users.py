from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from security import get_password_hash, verify_password
from models.users import UserCreate, User


async def register_user(session: AsyncSession, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    db_obj = User(**user_create.dict(), hash_password=hashed_password)
    session.add(db_obj)
    await session.commit()
    await session.refresh(db_obj)
    return db_obj


async def get_user_by_email_or_username(*, session: AsyncSession, email: str, username: str) -> User | None:
    statement = select(User).where(User.email == email or User.username == username)
    session_user = await session.execute(statement)
    return session_user.scalars().first()


async def authentication(session: AsyncSession, email_or_username: str, password: str) -> User:
    db_user = await get_user_by_email_or_username(session=session, email=email_or_username, username=email_or_username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hash_password):
        return None
    return db_user
