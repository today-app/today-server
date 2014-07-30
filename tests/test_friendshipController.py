# -*- coding: utf8 -*-

import os
from unittest import TestCase
from faker import Factory
from controllers.friendship import FriendshipController
from db import Connection, Post, PostComment, Friendship
from settings import Setting


class TestFriendshipController(TestCase):
    def setUp(self):
        super(TestFriendshipController, self).setUp()
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


    # def test_create(self):
    #     self.fail()

    def test_incoming(self):
        controller = FriendshipController()

        actor_id = 1
        target_id = 2
        self.assertEqual([], controller.incoming(target_id))
        self.assertTrue(controller.create(actor_id, target_id))
        self.assertEqual([actor_id], controller.incoming(target_id))


