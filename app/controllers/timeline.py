from gen.today import ttypes
from models.post_impl import PostImpl
from models.timeline_impl import UserTimelineImpl, HomeTimelineImpl
from utils import get_t_user


class TimelineController:
    def home(self, user_id):
        impl = HomeTimelineImpl()
        ret = []
        for post_id in impl.all_ids(pk=user_id):
            post = (PostImpl()).get(user_id, post_id)
            t_user = get_t_user(post.user_id)
            t_post = ttypes.Post(id=post_id, text=post.text.encode('utf-8'), user=t_user)
            ret.insert(0, t_post)

        return ret

    def user(self, user_id):
        impl = UserTimelineImpl()
        ret = []
        for post_id in impl.all_ids(pk=user_id):
            post = (PostImpl()).get(user_id, post_id)
            t_user = get_t_user(post.user_id)
            t_post = ttypes.Post(id=post_id, text=post.text.encode('utf-8'), user=t_user)
            ret.insert(0, t_post)

        return ret
