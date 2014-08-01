# -*- coding: utf8 -*-

import os
from unittest import TestCase
from faker import Factory
from controllers.post import PostController
from db import Connection, Post, PostComment, Friendship
from log import Logger
from settings import Setting

from gen.today import ttypes


class TestPostController(TestCase):
    def setUp(self):
        super(TestPostController, self).setUp()
        current_dir = os.path.dirname(os.path.abspath(__file__))

        setting = Setting()
        setting.initialize(os.path.join(current_dir, 'settings.cfg'))

        conn = Connection()
        conn.connect(setting.config)

        for collection in [Post, PostComment, Friendship]:
            collection.drop_collection()

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

    def test_comment_create(self):
        user_id = 1
        controller = PostController()
        post_id = controller.create(user_id, 'hello world')
        self.assertTrue(controller.comment_create(user_id, post_id, 'text'))

    def test_comment_list(self):
        user_id = 1
        controller = PostController()
        post_id = controller.create(user_id, 'hello world')
        comments0 = controller.comment_list(user_id, post_id)
        self.assertEqual(0, len(comments0))
        self.assertTrue(controller.comment_create(user_id, post_id, 'text'))

        comments1 = controller.comment_list(user_id, post_id)
        self.assertEqual(1, len(comments1))


