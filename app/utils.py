# -*- coding: utf8 -*-
import json

import re
from db import Connection
from gen.today import ttypes
from tasks import get_user


def cut_string(text, length=50):
    """
    :rtype : str
    :type text: str
    :type length: int
    """
    if len(text) > length:
        text = re.sub(r"\s+", " ", text)
        footer = "… "
        avail = length - len(footer)
        words = text.split()
        result = ""
        for word in words:
            word += " "
            if len(word) > avail:
                break
            result += word
            avail -= len(word)
        text = (result + footer).strip()

    return text


def get_next_id():
    conn = Connection()
    redis = conn.redis

    return redis.incr('current_post_id')


def get_t_user(user_id):
    redis = Connection().redis

    key = 'user:%d' % user_id
    user_json = redis.get(key)
    if user_json is None:
        user = (get_user.delay(user_id)).get()
        redis.set(key, json.dumps(user))
    else:
        user = json.loads(user_json)

    if user is not None:
        t_user = ttypes.User(id=user['id'], username=user['username'])
    else:
        t_user = None

    return t_user