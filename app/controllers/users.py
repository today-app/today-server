from twisted.internet import defer

from db import TwUser
from gen.today import ttypes


class UsersController:
    def get(self, user_id):
        def get_user_struct(user):
            id = user_id
            username = user[0].username
            print 'get_user_struct()'
            print (id, username)
            return ttypes.User(id=id, username=username)

        d = defer.maybeDeferred(TwUser.findBy, id=user_id)
        d.addCallback(get_user_struct)
        return d

    def get_by_username(self, username):
        def get_user_struct(user):
            id = user[0].id
            username = user[0].username
            print 'get_user_struct()'
            print (id, username)
            return ttypes.User(id=id, username=username)

        d = defer.maybeDeferred(TwUser.findBy, username=username)
        d.addCallback(get_user_struct)
        return d
