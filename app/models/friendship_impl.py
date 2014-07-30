from db import Friendship
from gen.today.ttypes import AlreadyExistsError
from models.model_impl import ModelImpl


class FriendshipImpl(ModelImpl):
    def create(self, actor_id, target_id):
        chk = Friendship.objects(actor_id=actor_id, target_id=target_id).first()
        if chk:
            raise AlreadyExistsError()

        friendship = Friendship(actor_id=actor_id, target_id=target_id, is_accepted=False)
        friendship.save()

        return True

    def incoming(self, user_id):
        """

        :type user_id: int
        :rtype bool
        """
        return Friendship.objects(target_id=user_id, is_accepted=False).all()
