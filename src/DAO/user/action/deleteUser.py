from DAO.connection import SESSION
from DAO.user.entity.userEntity import User


def delete_user(login):
    session = SESSION()
    user = session.query(User).filter_by(login=login).first()
    session.delete(user)
    session.commit()
    print('Юзер ' + str(user.login) + ' успешно удален')
