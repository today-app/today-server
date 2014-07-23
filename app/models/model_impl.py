from db import Connection


class ModelImpl(object):
    def __init__(self):
        conn = Connection()
        self.session = conn.session
        self.redis = conn.redis

