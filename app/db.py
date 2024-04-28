from sqlmodel import SQLModel, Session, create_engine, select

from models.users import User, UserCreate
from security import FIRST_SUPERUSER, FIRST_SUPERUSER_PASSWORD
from handlers.users import register_user


engine = create_engine("sqlite:///database.sqlite")


SQLModel.metadata.create_all(engine)


def init_db(session: Session) -> None:
    user = session.exec(
        select(User).where(User.email == FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=FIRST_SUPERUSER,
            password=FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = register_user(session=session, user_create=user_in)
