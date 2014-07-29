# -*- coding: utf8 -*-

from config import Config


class Setting(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Setting, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass

    def initialize(self, path):
        self.config = Config(file(path))


