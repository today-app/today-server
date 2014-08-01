# -*- coding: utf8 -*-
from db import Post, Connection, PostComment, Friendship, Timeline


class SystemController:
    def reset_fixtures(self):
        for collection in [Post, PostComment, Friendship, Timeline]:
            collection.drop_collection()

        (Connection()).redis.delete('current_post_id')

        return True
