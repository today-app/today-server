# -*- coding: utf8 -*-

import os
from unittest import TestCase
from faker import Factory
from controllers.post import PostController
from db import Connection, Post
from log import Logger
from settings import Setting

from gen.today import ttypes

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestPostController(TestCase):
    def setUp(self):
        super(TestPostController, self).setUp()

        setting = Setting()
        setting.initialize(os.path.join(current_dir, 'settings.cfg'))

        conn = Connection()
        conn.connect(setting.config)

        # initialize logger
        Logger.init(**setting.config.twisted.logging)

        Post.drop_collection()

        # Redis 초기화
        self.redis = conn.redis
        self.redis.delete('current_post_id')

        self.fake = Factory.create()

    def test_create(self):
        pc = PostController()

        self.assertRaises(TypeError, pc.create, 'one', 'foo')
        self.assertEqual(1, pc.create(1, 'hello world'))
        self.assertEqual(2, pc.create(1, 'sample post'))

    def test_get(self):
        pc = PostController()
        post_id = pc.create(1, 'hello world')
        post = pc.get(1, post_id)
        self.assertIsInstance(post, ttypes.Post)
        self.assertEqual(post_id, post.id)

        post_id = pc.create(1, 'hello world')
        post = pc.get(1, post_id)
        self.assertIsInstance(post, ttypes.Post)
        self.assertEqual(post_id, post.id)
        # self.assertTrue(pc.get())



