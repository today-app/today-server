from models.friendship_impl import FriendshipImpl


class FriendController:
    def ids(self, user_id):
        impl = FriendshipImpl()
        return impl.friend_ids(user_id)
