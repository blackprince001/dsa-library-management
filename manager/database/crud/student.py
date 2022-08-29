from sqlalchemy import select
from sqlalchemy.orm import Session

from manager.database.models import User as UserModel
from manager.database.schemas.users import UserCreate
from manager.security import Password


def create_user(db: Session, user: UserCreate) -> UserModel:
    db_user = UserModel(**user.dict())

    db_user.password = Password.hash(user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session) -> list[UserModel] | list:
    return db.scalars(select(UserModel).where(UserModel.is_admin == False)).all()


def get_admins(db: Session) -> list[UserModel] | list:
    return db.scalars(select(UserModel).where(UserModel.is_admin == True)).all()


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    return db.get(UserModel, user_id)


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    return db.scalar(select(UserModel).where(UserModel.username == username))
