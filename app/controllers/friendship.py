from models.friendship_impl import FriendshipImpl


class FriendshipController:
    def create(self, actor_id, target_id):
        return (FriendshipImpl()).create(actor_id, target_id)

    def incoming(self, user_id):
        ret = []
        for user in (FriendshipImpl()).incoming(user_id):
            ret = ret + [user.actor_id]
        return ret