from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from src.DAO.connection import BASE, ENGINE, SESSION

session_map = SESSION()

#   1: 'admin'
#   2: 'new'
#   3: 'redactor'
#   4: 'rejected'


class User(BASE):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    login = Column(String(40), unique=True, nullable=False)
    password = Column(String(40), nullable=False)

    role_id = Column(Integer, ForeignKey('role.id'), nullable=False, default=2)
    role = relationship('Role', backref=backref('user', lazy=True))

    def __init__(self, name, login, password, role_id=role_id):
        self.name = name
        self.login = login
        self.password = password


class Role(BASE):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Message(BASE):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    text = Column(Text(1024), nullable=False)
    time = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=1, nullable=False)
    color = Column(String(30), default='')

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=backref('message', lazy=True))

    def __init__(self, title, text, tags, user_id, color, status=0):
        self.title = title.strip()
        self.text = text.strip()
        self.tags = [
            Tag(text=tag.strip()) for tag in tags.split(',')
        ]
        self.user_id = user_id
        self.color = color
        self.status = status


class Tag(BASE):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    text = Column(Text(32), nullable=False)

    message_id = Column(Integer, ForeignKey('message.id'))
    message = relationship('Message', backref=backref('tags', lazy=True))


# BASE.metadata.create_all(ENGINE)


# roles = {1: 'admin',
#          2: 'new',
#          3: 'redactor',
#          4: 'rejected'
#          }

# for item in roles.keys():
#     id = item
#     name = roles[item]
#
#     set_all_roles = Role(name)
#
#     session_map.add(set_all_roles)
#
# user_admin = User('Vlad', 'admin', 'admin', 1)
# user_user = User('Nina', 'user', 'user', 2)
#
# session_map.add(user_admin)
# session_map.add(user_user)
#
# session_map.flush()
# session_map.commit()
#
#
# message_statuses = ('inreview',
#                     'aproved',
#                     'rejected'
#                     )






