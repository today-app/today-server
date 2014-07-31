from mongoengine import Q
from db import Friendship
from gen.today.ttypes import AlreadyExistsError, NotFoundError
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
        return list(Friendship.objects(target_id=user_id, is_accepted=False).all())

    def outgoing(self, user_id):
        """

        :type user_id: int
        :rtype bool
        """
        return list(Friendship.objects(actor_id=user_id, is_accepted=False).all())

    def accept(self, actor_id, target_id):
        request = Friendship.objects(actor_id=target_id, target_id=actor_id, is_accepted=False).first()
        if request is None:
            raise NotFoundError(why='friendship request not found.')

        request.is_accepted = True
        request.save()

        return True

    def cancel(self, actor_id, target_id):
        request = Friendship.objects(actor_id=actor_id, target_id=target_id, is_accepted=False).first()
        if request is None:
            raise NotFoundError()

        request.delete()
        return True

    def friend_ids(self, actor_id):
        friendship = Friendship.objects((Q(target_id=actor_id) | Q(actor_id=actor_id)) & Q(is_accepted=True)).all()

        ids = []
        for item in friendship:
            if item.actor_id == actor_id:
                ids.append(item.target_id)
            elif item.target_id == actor_id:
                ids.append(item.actor_id)

        return ids

