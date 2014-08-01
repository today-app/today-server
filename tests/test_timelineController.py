# -*- coding: utf8 -*-

import os
from unittest import TestCase
from faker import Factory
from controllers.post import PostController
from controllers.timeline import TimelineController
from db import Connection, Post, PostComment, Friendship, Timeline
from log import Logger
from settings import Setting

from gen.today import ttypes


class TesTimelineController(TestCase):
    def setUp(self):
        super(TesTimelineController, self).setUp()
        current_dir = os.path.dirname(os.path.abspath(__file__))

        setting = Setting()
        setting.initialize(os.path.join(current_dir, 'settings.cfg'))

        conn = Connection()
        conn.connect(setting.config)

        for collection in [Post, PostComment, Friendship, Timeline]:
            collection.drop_collection()

        # Redis 초기화
        self.redis = conn.redis
        self.redis.delete('current_post_id')

        self.fake = Factory.create()

    def test_list(self):
        timeline_controller = TimelineController()
        post_controller = PostController()
        actor_id = 1
        self.assertEqual([], timeline_controller.list(actor_id))
        post_id = post_controller.create(actor_id, 'sample text')
        posts = timeline_controller.list(actor_id)
        self.assertEqual(1, len(posts))

