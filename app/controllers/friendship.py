from gen.today import ttypes
from models.friendship_impl import FriendshipImpl


class FriendshipController:
    def create(self, actor_id, target_id):
        return (FriendshipImpl()).create(actor_id, target_id)

    def incoming(self, user_id):
        ret = []
        for user in (FriendshipImpl()).incoming(user_id):
            ret = ret + [user.actor_id]
        return ret

    def outgoing(self, user_id):
        ret = []
        for user in (FriendshipImpl()).outgoing(user_id):
            ret = ret + [user.target_id]
        return ret

    def accept(self, actor_id, target_id):
        # request = Friendship.objects(actor_id=target_id, target_id=actor_id, is_accepted=False).first()
        # if request is None:
        #     raise NotFoundError(why='friendship request not found.')
        #
        # request.is_accepted = True
        # request.save()
        #
        # raise ttypes.NotFoundError()
        impl = FriendshipImpl()
        return impl.accept(actor_id, target_id)

    def cancel(self, actor_id, target_id):
        impl = FriendshipImpl()
        return impl.cancel(actor_id, target_id)