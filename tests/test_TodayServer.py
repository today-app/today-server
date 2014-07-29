# -*- coding: utf8 -*-
import pprint
import time
import subprocess
from unittest import TestCase

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from genpy.today import TodayInternalApiService


pp = pprint.PrettyPrinter(indent=2)
host = 'localhost'
port = 9091


class TestPostController(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestPostController, cls).setUpClass()
        cls.proc1 = subprocess.Popen("../app/PythonServer.py", shell=True)
        time.sleep(2.0)

    def setUp(self):
        super(TestPostController, self).setUp()
        socket = TSocket.TSocket(host, port)
        self.transport = TTransport.TFramedTransport(socket)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = TodayInternalApiService.Client(protocol)
        self.transport.open()
        self.assertTrue(self.client.system_reset_fixtures())

    def tearDown(self):
        pass

    def test_post_create(self):
        res = self.client.post_create(1, 'hello')
        self.assertEqual(1, res)

    def test_post_comment_create(self):
        post_id = self.client.post_create(1, 'hello')
        self.assertEqual(1, post_id)

    @classmethod
    def tearDownClass(cls):
        super(TestPostController, cls).tearDownClass()
        cls.proc1.kill()
