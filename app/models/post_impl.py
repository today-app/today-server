import db
from utils import get_next_id

from models.model_impl import ModelImpl


class PostImpl(ModelImpl):
    def create(self, user_id, text):
        post_id = get_next_id()
        p = db.Post(post_id, user_id, text)
        p.save()

        return p.post_id

    def get(self, user_id, id):
        post = db.Post.objects(post_id=id).first()

        return post

    def list(self):
        return db.Post.objects.all()

