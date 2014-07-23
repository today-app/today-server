import db
from utils import get_next_id

from models.model_impl import ModelImpl


class PostImpl(ModelImpl):
    def create(self, user_id, text):
        post_id = get_next_id()
        p = db.Post(post_id, user_id, text)
        p.save()

        return p.post_id


