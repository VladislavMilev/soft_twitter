from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# ENGINE = create_engine('mysql+mysqlconnector://root:dofemu37@localhost/mini')

ENGINE = create_engine('mysql+mysqlconnector://44P2xsNIuE:FFFcC1Rc6S@remotemysql.com/44P2xsNIuE')
SESSION = sessionmaker(bind=ENGINE)
SESSION_SCOPE = scoped_session(SESSION)
BASE = declarative_base()


BASE.metadata.create_all(ENGINE)

# for instance in session.query(User).order_by(User.id):
#     print(instance.name)
