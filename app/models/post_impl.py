import db
from gen.today.ttypes import *
from models.timeline_impl import TimelineImpl
from utils import get_next_id

from models.model_impl import ModelImpl


class PostImpl(ModelImpl):
    def create(self, user_id, text):
        post_id = get_next_id()
        p = db.Post(post_id, user_id, text)
        p.save()

        t_impl = TimelineImpl()
        t_impl.distribute(user_id, p.to_dict())

        return p.post_id

    def get(self, user_id, post_id):
        post = db.Post.objects(post_id=post_id).first()

        return post

    def list(self):
        return db.Post.objects.all()

    def comment_create(self, user_id, post_id, text):
        pc = db.PostComment.objects(post_id=post_id).first()
        if not pc:
            pc = db.PostComment(post_id=post_id)
            pc.save()

        comment = db.Comment(user_id=user_id, text=text)
        pc.comments.append(comment)
        pc.save()

        return True

    def comment_list(self, post_id):
        pc = db.PostComment.objects(post_id=post_id).first()
        if not pc:
            return []

        return pc.comments

    def delete(self, user_id, post_id):
        post = db.Post.objects(post_id=post_id).first()
        if post is None:
            raise NotFoundError()

        post.delete()

        return True