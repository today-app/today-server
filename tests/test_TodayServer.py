# -*- coding: utf8 -*-
import pprint
import time
import subprocess
from unittest import TestCase

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from genpy.today import TodayInternalApiService
from genpy.today.ttypes import NotFoundError


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

    def test_post_delete(self):
        user_id = 1
        post_id = 1
        self.assertRaises(NotFoundError, self.client.post_delete, user_id, post_id)
        post_id = self.client.post_create(user_id, 'hello')
        posts = self.client.post_list(user_id)
        self.assertEqual(1, len(posts))
        self.assertTrue(self.client.post_delete(user_id, post_id))

    def test_post_list(self):
        user_id = 1
        post_id = self.client.post_create(user_id, 'hello')
        self.assertEqual(1, post_id)
        posts = self.client.post_list(user_id)
        self.assertEqual(1, len(posts))
        self.assertEqual(post_id, posts[0].id)
        post_id = self.client.post_create(user_id, 'hello')
        posts = self.client.post_list(user_id)
        self.assertEqual(2, len(posts))

    def test_post_comment_create(self):
        user_id = 1
        post_id = self.client.post_create(user_id, 'hello')
        self.assertTrue(self.client.post_comment_create(user_id, post_id, 'text'))

    def test_post_comment_list(self):
        user_id = 1
        post_id = self.client.post_create(user_id, 'hello')
        comments = self.client.post_comment_list(user_id, post_id)
        self.assertEqual(0, len(comments))

        self.assertTrue(self.client.post_comment_create(user_id, post_id, 'text'))
        comments = self.client.post_comment_list(user_id, post_id)
        self.assertEqual(1, len(comments))

    def test_friend_ids(self):
        actor_id = 1
        target_id = 2
        ids = self.client.friend_ids(actor_id)
        self.assertIsInstance(ids, list)
        self.assertEqual(0, len(ids))
        self.assertTrue(self.client.friendship_create(actor_id, target_id))
        self.assertTrue(self.client.friendship_accept(target_id, actor_id))
        self.assertEqual([target_id], self.client.friend_ids(actor_id))

    def test_friendship_request(self):
        actor_id = 1
        target_id = 2
        self.assertTrue(self.client.friendship_create(actor_id, target_id))

    def test_friendship_incoming(self):
        actor_id = 1
        target_id = 2
        self.assertEqual([], self.client.friendship_incoming(target_id))

        self.assertTrue(self.client.friendship_create(actor_id, target_id))
        self.assertEqual([actor_id], self.client.friendship_incoming(target_id))

    def test_friendship_outgoing(self):
        actor_id = 1
        target_id = 2
        self.assertEqual([], self.client.friendship_outgoing(actor_id))

        self.assertTrue(self.client.friendship_create(actor_id, target_id))
        self.assertEqual([target_id], self.client.friendship_outgoing(actor_id))

    def test_friendship_accept(self):
        actor_id = 1
        target_id = 2
        self.assertRaises(NotFoundError, self.client.friendship_accept, actor_id, target_id)
        self.assertTrue(self.client.friendship_create(actor_id, target_id))
        self.assertTrue(self.client.friendship_accept(target_id, actor_id))

    def test_friendship_cancel(self):
        actor_id = 1
        target_id = 2
        self.assertRaises(NotFoundError, self.client.friendship_cancel, actor_id, target_id)
        self.assertTrue(self.client.friendship_create(actor_id, target_id))
        self.assertTrue(self.client.friendship_cancel(actor_id, target_id))

    def test_friendship_reject(self):
        actor_id = 1
        target_id = 2
        self.assertRaises(NotFoundError, self.client.friendship_reject, actor_id, target_id)
        self.assertTrue(self.client.friendship_create(target_id, actor_id))
        self.assertIn(target_id, self.client.friendship_incoming(actor_id))
        self.assertTrue(self.client.friendship_reject(actor_id, target_id))
        self.assertNotIn(target_id, self.client.friendship_incoming(actor_id))

    def test_timeline_list(self):
        actor_id = 1
        self.assertEqual([], self.client.timeline_list(actor_id))
        # self.assertEqual(1, len(self.client.timeline_list(actor_id)))
        post_id = self.client.post_create(actor_id, 'sample text')
        self.assertEqual(1, len(self.client.timeline_list(actor_id)))
        post_id = self.client.post_create(actor_id, '한글 테스트')
        posts = self.client.timeline_list(actor_id)
        self.assertEqual(2, len(posts))

    @classmethod
    def tearDownClass(cls):
        super(TestPostController, cls).tearDownClass()
        cls.proc1.kill()
