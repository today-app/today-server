# -*- coding: utf8 -*-
from db import Post, Connection, PostComment


class SystemController:
    def reset_fixtures(self):
        Post.drop_collection()
        PostComment.drop_collection()
        (Connection()).redis.delete('current_post_id')

        return True
