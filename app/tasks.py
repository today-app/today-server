#import os
#from datetime import timedelta

#from celery import Celery
#from mongoengine import connect

#from db import Connection
#from log import Logger
#from models.letter_impl import LetterImpl
#from settings import Setting


#current_dir = os.path.dirname(os.path.abspath(__file__))

#setting = Setting()
#setting.initialize(os.path.join(current_dir, 'settings.cfg'))

#conn = Connection()
#conn.connect(setting.config)

## initialize logger
#Logger.init(**setting.config.twisted.logging)

## connect to mongoengine
#connect(setting.config.mongoengine.database, **setting.config.mongoengine.kwargs)

#app = Celery('tasks', broker=setting.config.celery.broker)
#CELERYBEAT_SCHEDULE = {
    #'publish_scheduled-every-1-minutes': {
        #'task': 'tasks.publish_scheduled',
        #'schedule': timedelta(seconds=10),
        #'args': ()
    #},
#}

#CELERY_TIMEZONE = 'UTC'

#app.conf.update(
    #CELERY_RESULT_BACKEND=setting.config.celery.result_backend,
    #BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 3600}  # 1 hour.
#)
#app.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)
#app.conf.update(CELERY_TIMEZONE=CELERY_TIMEZONE)


#@app.task
#def publish_scheduled():
    #Logger.info('publish_scheduled')

    #impl = LetterImpl()
    #return impl.publish_scheduled()
