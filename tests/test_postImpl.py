# -*- coding: utf8 -*-

import os
from unittest import TestCase

from faker import Factory

from db import Connection, Post, PostComment
from log import Logger
from models.post_impl import PostImpl
from settings import Setting


current_dir = os.path.dirname(os.path.abspath(__file__))


class TestPostImpl(TestCase):
    def setUp(self):
        super(TestPostImpl, self).setUp()
        setting = Setting()
        setting.initialize(os.path.join(current_dir, 'settings.cfg'))

        conn = Connection()
        conn.connect(setting.config)

        Post.drop_collection()
        PostComment.drop_collection()

        # Redis 초기화
        self.redis = conn.redis
        self.redis.delete('current_post_id')

        self.fake = Factory.create()

    def test_create(self):
        pi = PostImpl()
        # 0. text='foo', user_id=1 생성 성공
        user_id = 1
        self.assertEqual(1, pi.create(user_id, self.fake.sentence()))
        self.assertEqual(2, pi.create(user_id, self.fake.sentence()))

        self.assertEqual(2, len(Post.objects.all()))
        # 1. 포스트 생성하면 db에 저장되어야함

        # 2. 잘못된 내용으로는 생성 안될 것.
        # 3. 10회 생성해보고 db에 11개 있을 것

    def test_comment_create(self):
        model = PostImpl()
        post_id = model.create(1, 'hello')
        post = model.get(1, post_id)
        self.assertEqual(post.post_id, post_id)

        self.assertTrue(model.comment_create(1, post_id, 'text'))

    def test_comment_list(self):
        model = PostImpl()
        post_id = model.create(1, 'hello')

        model.comment_create(1, post_id, 'text')

        comments = model.comment_list(post_id)
        self.assertEqual(1, len(comments))
