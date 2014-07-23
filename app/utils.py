# -*- coding: utf8 -*-

import re
from db import Connection


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