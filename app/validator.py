from datetime import datetime
import re
import urlparse
import string

from voluptuous import Schema, Required, All, Invalid, Length, Range, Any, Optional, MultipleInvalid
from log import Logger


def Url(msg=None):
    def f(v):
        """Verify that the value is a URL."""
        try:
            pieces = urlparse.urlparse(v)
            if all([pieces.scheme, pieces.netloc]) and \
               set(pieces.netloc) <= set(string.letters + string.digits + '-.') and \
               pieces.scheme in ['http', 'https']:
                return str(v)
            else:
                raise Invalid(msg or ("incorrect URL"))
        except:
            raise Invalid(msg or ("incorrect URL"))

    return f

def IntList(msg=None):
    def f(v):
        try:
            assert isinstance(v, list)
            for i in v:
                assert isinstance(i, int)
            return v
        except:
            raise Invalid(msg or ("incorrect target_user_ids"))

    return f


def DateTime(fmt='%Y-%m-%d %H:%M:%S'):
    return lambda v: datetime.strptime(v, fmt)


class Validator:

    validate_comment = Schema({
        Required('id'): Any(str, unicode),
        Required('user_id'): All(int, Range(min=1)),
        Required('content'): All(Any(str, unicode), Length(min=4)),
    })

    validate_link = Schema({
        Required('title'): Any(str, unicode),
        Required('url'): All(Url())
    })

    validate_bgmusic = Schema({
        Required('url'): All(Url())
    })

    validate_letter = Schema({
        Required('letter_id'): All(int, Range(min=1)),
        Optional('orig_id'): All(Any(str, unicode), Length(min=24)),
        Required('user_id'): All(int, Range(min=1)),

        Required('is_public'): All(bool),
        Required('is_published'): All(bool),
        Required('is_deleted'): All(bool),
        Optional('is_scheduled'): All(bool),

        Required('type'): Any('plain', 'book', 'photo', 'video', 'voice'),

        Optional('category_id'): All(int, Range(min=1)),
        Optional('cheer_id'): All(int, Range(min=1)),
        Optional('draft_mailbox_id'): All(Any(str, unicode)),

        # Required('target'): Any('public', 'subscriber', 'friend', 'me'),
        # Optional('target_user_ids'): Any('public', 'subscriber', 'friend', 'me'),
        # Optional('target_email'): Any(str, unicode),

        Required('title'): All(Any(str, unicode), Length(min=4)),
        Required('text'): All(Any(str, unicode), Length(min=4)),

        Optional('link'): {
            Required('title'): Any(str, unicode),
            Required('url'): All(Url())
        },

        Optional('bg_music'): {
            Required('url'): All(Url())
        },

        # Required('created_dt'): DateTime(),
        Required('created_dt'): All(Any(str, unicode)),
        Optional('modified_dt'): DateTime(),
        # Optional('published_dt'): DateTime(),
        Optional('published_dt'): All(Any(str, unicode)),

        Optional('tags'): All(Any(str, unicode)),
        # Optional('photos'): Any(list),
        # Optional('id'): Any(str, unicode),
        # Optional('target'): Any('public', 'subscriber', 'friend', 'me'),
        # Optional('target_user_ids'): Any(list),
        # Optional('target_email'): Any(str, unicode),
        # Optional('target_email'): Any(str, unicode),
    }, extra=True)

    validate_filter = Schema({
        Optional('category_id'): int,
        Optional('cheer_id'): int,
        Optional('user_id'): int,
    })

    validate_letter_all_params = Schema({
        Optional('limit'): All(int, Range(min=1)),
        Optional('max_id'): All(int, Range(min=1)),
        Optional('since_id'): All(int, Range(min=1))
    })

    validate_bookquote_element = Schema({
        Required('book'): {
            Required('id'): All(int, Range(min=1)),
            Required('title'): All(Any(str, unicode), Length(min=1)),
            Required('cover_url'): All(Url()),
            Required('author'): All(Any(str, unicode), Length(min=1)),
        },
        Required('quote'): All(Any(str, unicode), Length(min=4)),
        Required('text'): All(Any(str, unicode), Length(min=4)),
    })

    validate_voice_element = Schema({
        Required('url'): All(Url())
    })

    validate_video_element = Schema({
        Required('type'): Any('youtube', 'vimeo'),
        Required('url'): All(Url())
    })

    validate_photo_element = Schema({
        Optional('id'): All(Any(str, unicode)),
        Required('url'): All(Url()),
        Required('path'): All(Any(str, unicode), Length(min=1)),
        Required('width'): All(int, Range(min=1)),
        Required('height'): All(int, Range(min=1)),
    })

    validate_paging_params = Schema({
        Optional('limit'): All(int, Range(min=1)),
        Optional('max_id'): All(int, Range(min=1)),
        Optional('min_id'): All(int, Range(min=1))
    })

    @staticmethod
    def validate_letter_target(params):
        try:
            target = params['target']
            if target not in ['public', 'friend', 'subscriber', 'me', 'users', 'email']:
                raise MultipleInvalid('hello')

            elif target == 'public':
                assert isinstance(params['category_id'], int)
                assert params['category_id'] > 0
            elif target == 'users':
                assert isinstance(params['user_ids'], list)
                assert len(params['user_ids']) > 0
                for id in params['user_ids']:
                    assert isinstance(id, int)
            elif target == 'email':
                Logger.debug('x')
                assert isinstance(params['email'], unicode) or  isinstance(params['email'], str)

            return True
        except Exception as e:
            Logger.debug('y')
            raise MultipleInvalid(str(e))


# def Email(msg=None):
#     def f(v):
#         if re.match("[\w\.\-]*@[\w\.\-]*\.\w+", str(v)):
#             return str(v)
#         else:
#             raise Invalid(msg or ("incorrect email address"))
#
#     return f
