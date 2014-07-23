#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import re

from zope.interface import implements
from twisted.internet import reactor
from thrift.transport import TTwisted

from db import Connection
from log import Logger
from settings import Setting


current_dir = os.path.dirname(os.path.abspath(__file__))

from gen.today import TodayInternalApiService
from gen.today.ttypes import *


class TodayInternalApiServiceHandler:
    implements(TodayInternalApiService.Iface)

    def __init__(self):
        Logger.info('LetterApiService started.')

    def __getattr__(self, item):
        Logger.info(item)
        item = re.split('_', item)
        module_name, mthd = item[0], '_'.join(item[1:])

        class_name = module_name.capitalize() + 'Controller'

        module = __import__('controllers.%s' % module_name)
        instance = getattr(getattr(module, module_name), class_name)()

        return getattr(instance, mthd)


if __name__ == '__main__':
    setting = Setting()
    setting.initialize(os.path.join(current_dir, 'settings.cfg'))

    conn = Connection()
    conn.connect(setting.config)

    # initialize logger
    Logger.init(**setting.config.twisted.logging)

    # setup server
    handler = TodayInternalApiServiceHandler()
    processor = TodayInternalApiService.Processor(handler)
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = reactor.listenTCP(setting.config.twisted.port,
                               TTwisted.ThriftServerFactory(processor, pfactory),
                               interface=setting.config.twisted.interface)

    reactor.run()
