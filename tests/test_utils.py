# -*- coding: utf8 -*-

import os
from unittest import TestCase

from db import Connection
from log import Logger
from settings import Setting
from utils import get_next_id


current_dir = os.path.dirname(os.path.abspath(__file__))


class TestUtils(TestCase):
    def setUp(self):
        super(TestUtils, self).setUp()
        setting = Setting()
        setting.initialize(os.path.join(current_dir, 'settings.cfg'))

        conn = Connection()
        conn.connect(setting.config)

        # initialize logger
        Logger.init(**setting.config.twisted.logging)

        # Redis 초기화
        self.redis = conn.redis
        self.redis.delete('current_post_id')


    def test_get_next_id(self):
        self.assertEqual(1, get_next_id())
        self.assertEqual(2, get_next_id())
