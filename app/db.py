import json
from datetime import datetime

import redis
from mongoengine import connect, Document, IntField, DateTimeField, EmbeddedDocument, StringField, \
    EmbeddedDocumentField, ListField, BooleanField

from twistar.dbobject import DBObject
from twistar.registry import Registry
from twisted.enterprise import adbapi

from sqlalchemy import Column, Integer, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Connection(object):
    is_connected = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        pass

    def connect(self, config=None):
        if config is not None:
            # connect mysql
            engine = create_engine(config.sqlalchemy.uri, **config.sqlalchemy.kwargs)
            self.session = (sessionmaker(bind=engine))()

            Registry.DBPOOL = adbapi.ConnectionPool('MySQLdb', user="user", passwd="secret", db="today_web")

            # connect mongodb
            connect(config.mongoengine.database, **config.mongoengine.kwargs)

            # connect redis
            self.redis = redis.StrictRedis(host=config.redis.host, port=config.redis.port, db=config.redis.db)

            # TODO: validate
            self.is_connected = True


class Comment(EmbeddedDocument):
    id = StringField()
    user_id = IntField()
    text = StringField()
    created_dt = DateTimeField()


class Post(Document):
    post_id = IntField(required=True)
    user_id = IntField(required=True)
    text = StringField()

    def to_dict(self):
        data = json.loads(self.to_json())
        data['id'] = str(self.id)

        del data['_id']
        # del data['_cls']

        # created_dt = int(data['created_dt']['$date'] / 1000)
        # try:
        # data['created_dt'] = datetime.fromtimestamp(created_dt).strftime('%Y-%m-%d %H:%M:%S.%f')
        # except Exception as e:
        #     data['created_dt'] = '1970-01-01 00:00:00.000'
        #
        # if 'published_dt' in data:
        #     published_dt = int(data['published_dt']['$date'] / 1000)
        #     try:
        #         data['published_dt'] = datetime.fromtimestamp(published_dt).strftime('%Y-%m-%d %H:%M:%S.%f')
        #     except Exception as e:
        #         data['published_dt'] = '1970-01-01 00:00:00.000'
        # else:
        #     data['published_dt'] = ''

        return data


class PostComment(Document):
    post_id = IntField(required=True)
    comments = ListField(EmbeddedDocumentField(Comment))


class Friendship(Document):
    actor_id = IntField(required=True)
    target_id = IntField(required=True)
    is_accepted = BooleanField(required=True)


class TimelineItem(EmbeddedDocument):
    type = StringField()
    item_id = IntField()
    key = IntField()


class Timeline(Document):
    user_id = IntField(required=True, unique=True)
    items = ListField(EmbeddedDocumentField(TimelineItem))
    created_dt = DateTimeField()
    meta = {'allow_inheritance': True}

    def to_dict(self):
        data = json.loads(self.to_json())
        data['id'] = str(self.id)

        del data['_id']
        del data['_cls']

        created_dt = int(data['created_dt']['$date'] / 1000)
        try:
            data['created_dt'] = datetime.fromtimestamp(created_dt).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            data['created_dt'] = '1970-01-01 00:00:00'

        return data


class TwUser(DBObject):
    TABLENAME = 'users'

# SQLAlchemy Models
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'MyISAM'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(16))
    password = Column('password', String(255))
    role = Column('role', String(16))
    created = Column(DateTime, default=datetime.now)

    @property
    def serialize(self):
        return {
            'id': int(self.id),
            'username': self.username,
        }

