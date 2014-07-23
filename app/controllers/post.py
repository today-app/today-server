# -*- coding: utf8 -*-

from gen.today import ttypes
from models.post_impl import PostImpl


class PostController:
    def create(self, user_id, text):
        """
        User<user_id>의 신규 Post 작성

        :rtype : int
        :type user_id: int
        :type text: str
        """
        try:
            assert isinstance(user_id, int)
            assert isinstance(text, str)
        except AssertionError as e:
            raise TypeError

        return (PostImpl()).create(user_id, text)

    def get(self, user_id, post_id):
        """
        Post<post_id>의 상세정보 조회

        :rtype : ttypes.Post
        :type user_id: int
        :type text: str
        """
        post = (PostImpl()).get(user_id=user_id, id=post_id)
        return ttypes.Post(id=post.post_id, text=post.text)

    def list(self, user_id):
        """
        전체 Post 목록 조회

        :rtype : list of ttypes.Post
        """

        ret = []
        for post in (PostImpl()).list():
            t_user = ttypes.User(id=1, username='foo')
            t_post = ttypes.Post(id=post.post_id, text=post.text, user=t_user)
            ret = ret + [t_post]

        return ret

