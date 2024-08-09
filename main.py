from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    email: str

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    profession: str
    description: str
    user_id: int = Field(foreign_key='user.id')


engine = create_engine('sqlite:///database.db')
SQLModel.metadata.create_all(engine)

class Connetion:
    def __init__(self) -> None:
        self.session = Session(engine)

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.close()


def create_user(user: User, profile: Profile = None):
    with Connetion() as conn:
        conn.add(user)
        conn.commit()
        conn.refresh(user)

        if profile:
            profile.user_id = user.id
            conn.add(profile)
            conn.commit()

def get_all_users(profiles: bool = None):
    with Connetion() as conn:
        if profiles:
            query = select(User, Profile).join(Profile).where(User.id == Profile.user_id)
            users = conn.exec(query).all()
            return users
        
        query = select(User)
        users = conn.exec(query).all()
        return users

user = User(name="Hállan", email="hallan@neves.com")
profile = Profile(profession='Dev', description='Coda fofo')

# create_user(user, profile)
# print(get_all_users(profiles=False))
