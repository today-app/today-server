import os
from datetime import timedelta

from celery import Celery
from mongoengine import connect

from db import Connection, User
from log import Logger
from models.friendship_impl import FriendshipImpl
from models.timeline_impl import UserTimelineImpl, HomeTimelineImpl
from settings import Setting


current_dir = os.path.dirname(os.path.abspath(__file__))

setting = Setting()
setting.initialize(os.path.join(current_dir, 'settings.cfg'))

conn = Connection()
conn.connect(setting.config)

# initialize logger
Logger.init(**setting.config.twisted.logging)

app = Celery('tasks', broker=setting.config.celery.broker)
# CELERYBEAT_SCHEDULE = {
#     'publish_scheduled-every-1-minutes': {
#         'task': 'tasks.publish_scheduled',
#         'schedule': timedelta(seconds=10),
#         'args': ()
#     },
# }

CELERY_TIMEZONE = 'UTC'

app.conf.update(
    CELERY_RESULT_BACKEND=setting.config.celery.result_backend,
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600}  # 1 hour.
)
# app.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)
app.conf.update(CELERY_TIMEZONE=CELERY_TIMEZONE)

@app.task
def get_user(user_id):
    Logger.info('get_user')
    session = Connection().session
    user = session.query(User).get(user_id)
    if not user:
        return None

    return user.serialize


@app.task(ignore_result=True)
def fanout(p):
    print 'fanout(): %s' % p.to_dict()

    (UserTimelineImpl()).distribute(p.user_id, p.to_dict())
    for user_id in (FriendshipImpl()).friend_ids(p.user_id) + [p.user_id]:
        (HomeTimelineImpl()).distribute(user_id, p.to_dict())

    print 'fanout(): done... '