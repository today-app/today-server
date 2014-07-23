from gen.today import ttypes
from models.post_impl import PostImpl


class PostController:
    def create(self, user_id, text):
        """


        :rtype : int
        :type user_id: int
        :type text: str
        """
        try:
            assert isinstance(user_id, int)
        except AssertionError as e:
            raise TypeError

        pi = PostImpl()
        return pi.create(user_id, text)

        # def get(self, user_id, post_id):
        # Logger.info('post.get()')
        #     return PostImpl().get(post_id)

    def get(self, user_id, post_id):

        return ttypes.Post(id=post_id)
