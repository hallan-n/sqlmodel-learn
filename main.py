from sqlmodel import Relationship, SQLModel, Field, create_engine, Session
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    email: str
    profile: Optional["Profile"] = Relationship(back_populates="user")


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    profession: str
    description: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="profile")


engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)


def create_user(user: User, profile: Profile = None):
    with Session(engine) as conn:
        conn.add(user)
        conn.commit()
        conn.refresh(user)

        if profile:
            profile.user_id = user.id
            conn.add(profile)
            conn.commit()


def update_user(user: User):
    with Session(engine) as conn:
        existing_user = conn.get(User, user.id)
        if existing_user:
            merged_user = conn.merge(user)
            conn.commit()
            conn.refresh(merged_user)
            return merged_user


def get_user(id: int):
    with Session(engine) as conn:
        user = conn.get(User, id)
        return user, user.profile


def delete_user(id: int):
    with Session(engine) as conn:
        user = conn.get(User, id)
        if user:
            conn.delete(user.profile)
            conn.delete(user)
            conn.commit()
