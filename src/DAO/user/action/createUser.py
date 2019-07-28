from DAO.connection import SESSION
from DAO.user.entity.userEntity import User


def add_user(name, login, password):
    session = SESSION()
    user = User(name=name,
                login=login,
                password=password
                )
    session.add(user)
    session.commit()
