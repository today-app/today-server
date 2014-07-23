#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#
import os
from mongoengine import connect
from thrift.protocol import TBinaryProtocol

from twisted.application import internet, service
from thrift.transport import TTwisted

from db import Connection
from letter import LetterApiService
from letter.ttypes import *
from PythonServer import LetterApiServiceHandler
from log import Logger
from settings import Setting


def make_application():
    application = service.Application('LetterApiService')

    setting = Setting()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    setting.initialize(os.path.join(current_dir, 'settings.cfg'))

    conn = Connection()
    conn.connect(setting.config)

    # initialize logger
    Logger.init(**setting.config.twisted.logging)

    # connect to mongoengine
    connect(setting.config.mongoengine.database, **setting.config.mongoengine.kwargs)

    handler = LetterApiServiceHandler(conn=conn)
    processor = LetterApiService.Processor(handler)

    serverFactory = TTwisted.ThriftServerFactory(processor,
                                                 TBinaryProtocol.TBinaryProtocolFactory())

    apiService = internet.TCPServer(setting.config.twisted.port, serverFactory)

    multiService = service.MultiService()
    apiService.setServiceParent(multiService)
    multiService.setServiceParent(application)

    return application


application = make_application()
