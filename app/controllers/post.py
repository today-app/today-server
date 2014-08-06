# -*- coding: utf8 -*-

from gen.today import ttypes
from models.post_impl import PostImpl
from utils import get_t_user


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
        post = (PostImpl()).get(user_id=user_id, post_id=post_id)
        t_user = get_t_user(post.user_id)

        return ttypes.Post(id=post.post_id, text=post.text.encode('utf-8'), user=t_user)

    def list(self, user_id):
        """
        전체 Post 목록 조회

        :rtype : list of ttypes.Post
        """

        ret = []
        for post in (PostImpl()).list():
            t_user = get_t_user(post.user_id)
            t_post = ttypes.Post(id=post.post_id, text=post.text.encode('utf-8'), user=t_user)
            ret.insert(0, t_post)
        return ret


    def delete(self, user_id, post_id):
        return (PostImpl()).delete(user_id, post_id)
        # raise ttypes.NotFoundError()

    def comment_create(self, user_id, post_id, text):
        return (PostImpl()).comment_create(user_id, post_id, text)

    def comment_list(self, user_id, post_id):
        ret = []
        comments = (PostImpl()).comment_list(post_id)
        for comment in comments:
            t_user = get_t_user(comment.user_id)
            t_comment = ttypes.Comment(user=t_user, text=comment.text.encode('utf-8'))
            ret = ret + [t_comment]

        return ret



