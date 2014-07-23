# -*- coding: utf8 -*-
from db import Post, Connection


class SystemController:
    def reset_fixtures(self):
        Post.drop_collection()
        (Connection()).redis.delete('current_post_id')

        return True
