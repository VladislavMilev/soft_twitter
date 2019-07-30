from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from DAO.connection import BASE, ENGINE


class User(BASE):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    login = Column(String(40), unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    role = Column(String(10), nullable=False, default='user')

    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password


class Message(BASE):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    text = Column(Text(1024), nullable=False)
    time = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref=backref('message', lazy=True))

    def __init__(self, title, text, tags, user_id):
        self.title = title.strip()
        self.text = text.strip()
        self.tags = [
            Tag(text=tag.strip()) for tag in tags.split(',')
        ]
        self.user_id = user_id


class Tag(BASE):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    text = Column(Text(32), nullable=False)

    # message_id = Column(Integer, ForeignKey('message.id'))
    message_id = Column(Integer, ForeignKey('message.id'), nullable=False)
    message = relationship('Message', backref=backref('tags', lazy=True))


BASE.metadata.create_all(ENGINE)
