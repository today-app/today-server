import os
from sys import stdout
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from config import Config


class Logger:
    filename = 'twistd.log'
    log_level = 2
    target = 'stdout'

    def __init__(self):
        pass

    @classmethod
    def init(cls, target='stdout', log_level=2, filename='twistd.log'):
        cls.filename = filename
        cls.target = target
        cls.log_level = log_level

        if cls.target is 'file':
            logfile = get_filename(filename=cls.filename)
            log.startLogging(DailyLogFile.fromFullPath(logfile))
        else:
            log.startLogging(stdout)

    @classmethod
    def info(cls, msg):
        if cls.log_level >= 1:
            cls._msg(msg, keyword='info')

    @classmethod
    def warn(cls, msg):
        cls._msg(msg, keyword='warn')

    @classmethod
    def debug(cls, msg):
        if cls.log_level >= 2:
            if not isinstance(msg, str):
                import pprint
                #from inspect import getmembers

                #pp = pprint.PrettyPrinter(indent=2)
                #msg = pp.pformat(getmembers(msg))
                msg = pprint.pformat(msg)

            cls._msg(msg, keyword='debug')

    @classmethod
    def err(cls, msg):
        cls._msg(msg, keyword='error')

    @classmethod
    def msg(cls, msg):
        if cls.log_level >= 1:
            cls._msg(msg)

    @classmethod
    def _msg(cls, msg, keyword=None):
        if keyword:
            keyword = '[%s] ' % (keyword.upper())
        else:
            keyword = ''
        log.msg('%s%s' % (keyword, msg))


def get_filename(filename='service.log'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logfile = os.path.join(os.path.dirname(current_dir), 'logs', filename)
    return logfile


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    cfg = Config(file(os.path.join(current_dir, 'log.cfg')))

    Logger.init(**cfg)
    Logger.info('some info.')
    Logger.msg('some message.')
    Logger.warn('some warning.')
    Logger.err('error uccured.')
    Logger.debug(1)
    Logger.debug('some string')
