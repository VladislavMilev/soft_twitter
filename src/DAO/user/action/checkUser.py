from DAO.connection import SESSION
from DAO.user.entity.userEntity import User


def identify(login):
    session = SESSION()
    try:
        user_f = session.query(User).filter_by(login=login).first()
        if user_f:
            print('role - admin')
        else:
            print('role - user')
    except:
        print('Юзер не найден')


