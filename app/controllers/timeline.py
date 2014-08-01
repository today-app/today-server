from gen.today import ttypes
from models.post_impl import PostImpl
from models.timeline_impl import TimelineImpl


class TimelineController:
    def list(self, user_id):
        impl = TimelineImpl()
        ret = []
        for post_id in impl.all_ids(pk=user_id):
            post = (PostImpl()).get(user_id, post_id)
            t_user = ttypes.User(id=1, username='dummy')
            t_post = ttypes.Post(id=post_id, text=post.text.encode('utf-8'), user=t_user)

            ret.append(t_post)

        return ret
