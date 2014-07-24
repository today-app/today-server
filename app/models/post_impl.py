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


    def comment_create(self, user_id, post_id, text):
        post = db.Post.objects(post_id=post_id).first()
        comment = db.Comment(user_id=user_id, text=text)
        post.comments.append(comment)
        post.save()

        return True
        # letter_comment = LetterComment.objects(letter_id=letter_id).first()
        # if not letter_comment:
        #     letter_comment = LetterComment(letter_id=letter_id)
        #     letter_comment.save()
        #
        # Logger.debug(str(letter_comment.comments))
        # letter_comment.comments.append(Comment(**comment))
        # letter_comment.save()
