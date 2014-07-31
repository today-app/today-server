# -*- coding: utf8 -*-

import os
from unittest import TestCase

from faker import Factory

from db import Connection, Post, PostComment, Friendship
from gen.today import ttypes
from models.friendship_impl import FriendshipImpl
from settings import Setting


current_dir = os.path.dirname(os.path.abspath(__file__))


class TestFriendshipImpl(TestCase):
    def setUp(self):
        super(TestFriendshipImpl, self).setUp()
        setting = Setting()
        setting.initialize(os.path.join(current_dir, 'settings.cfg'))

        conn = Connection()
        conn.connect(setting.config)

        Post.drop_collection()
        PostComment.drop_collection()
        Friendship.drop_collection()

        # Redis 초기화
        self.redis = conn.redis
        self.redis.delete('current_post_id')

        self.fake = Factory.create()

    def test_create(self):
        impl = FriendshipImpl()
        actor_id = 1
        target_id = 2
        self.assertTrue(impl.create(actor_id, target_id))
        self.assertRaises(ttypes.AlreadyExistsError, impl.create, actor_id, target_id)

    def test_outgoing(self):
        impl = FriendshipImpl()
        actor_id = 1
        target_id = 2
        ids = impl.outgoing(actor_id)
        self.assertIsInstance(ids, list)
        self.assertEqual(0, len(ids))

        self.assertTrue(impl.create(actor_id, target_id))
        ids = impl.outgoing(actor_id)
        self.assertEqual(1, len(ids))

    def test_accept(self):
        impl = FriendshipImpl()
        actor_id = 1
        target_id = 2

        self.assertRaises(ttypes.NotFoundError, impl.accept, target_id, actor_id)
        self.assertTrue(impl.create(actor_id, target_id))
        self.assertTrue(impl.accept(target_id, actor_id))