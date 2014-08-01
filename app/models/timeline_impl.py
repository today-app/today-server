# -*- coding: utf8 -*-
import datetime
import time
from db import Timeline, TimelineItem

from gen.today.ttypes import InputValidationError
from log import Logger
from models.model_impl import ModelImpl


class AbstractTimelineImpl(ModelImpl):
    pk = 'user_id'

    def create(self, pk=None):
        timeline_class = self.get_timeline_class()
        if not pk:
            raise ValueError('pk should not None.')

        created_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        kwargs = dict()
        kwargs[self.pk] = pk
        kwargs['created_dt'] = created_dt

        timeline = timeline_class(**kwargs)
        timeline.save()
        return str(timeline.id)

    def get(self, obj_id):
        timeline_class = self.get_timeline_class()
        timeline = timeline_class.objects(id=obj_id).order_by('-items__key').first()

        return timeline.to_dict()

    def get_items(self, pk=None, max_id=None, min_id=None, limit=None, filter=None):
        timeline_class = self.get_timeline_class()

        collection = timeline_class._get_collection()

        if pk is not None:
            _match = [{"$match": {self.pk: pk}}]
        else:
            raise ValueError('pk should not None.')

        _unwind = [{"$unwind": "$items"}]
        _sort = [{"$sort": {"items.key": -1}}]
        _search = []
        _limit = []

        try:
            if filter is not None and isinstance(filter, dict):
                for key, value in filter.iteritems():
                    items_type = "items.%s" % key
                    _search = _search + [{"$match": {items_type: value}}]
        except Exception as e:
            Logger.debug(type(e))
            Logger.debug(str(e))
            raise e

        if max_id is not None:
            _search = _search + [{"$match": {"items.key": {"$lt": max_id}}}]
        if min_id is not None:
            _search = _search + [{"$match": {"items.key": {"$gt": min_id}}}]
        if limit is not None:
            _limit = [{"$limit": limit}]

        _group = [{"$group": {"_id": "$_id", "items": {"$push": "$items"}}}]
        params = _match + _unwind + _sort + _search + _limit + _group
        result = collection.aggregate(params)

        try:
            items = result['result'][0]['items']
            return items
        except IndexError:
            Logger.debug('PersonalTimeline.get_items 7')
            return []

    def prepend(self, pk=None, **kwargs):
        Logger.debug('> prepend')
        Logger.debug('> ' + str(kwargs))
        if not pk:
            raise ValueError('pk should not be None.')

        try:
            timeline_class = self.get_timeline_class()

            key = int(time.time() * 1000)
            # key = key
            item = self.make_items(**kwargs)

            _filter = {}
            _filter[self.pk] = pk

            timeline = timeline_class.objects(**_filter).first()
            if not timeline:
                data = dict(pk=pk)

                obj_id = self.create(**data)
                timeline = timeline_class.objects(id=obj_id).first()

            timeline.update(push__items=item)
        except InputValidationError as e:
            Logger.debug('< prepend - InputValidationError')
            return False

        Logger.debug('< prepend end')
        return True

    def delete(self, pk=None, key=None):
        if pk is None or key is None:
            raise ValueError('pk, key should not None.')

        timeline_class = self.get_timeline_class()
        _filter = {}
        _filter[self.pk] = pk

        return timeline_class.objects(**_filter).update_one(upsert=True, pull__items__key=key)

    def validate(self, **kwargs):
        raise NotImplementedError

    def get_timeline_class(self):
        raise NotImplementedError

    def get_item_class(self):
        raise NotImplementedError

    def make_items(self, **kwargs):
        self.validate(**kwargs)
        try:
            item_class = self.get_item_class()
            item = item_class(**kwargs)
            return item
        except Exception as e:
            Logger.debug(str(e))

    def chk_item_exists(self, pk=None, field=None, value=None):
        return self.get_item_by_field(pk=pk, field=field, value=value) is not None

    def get_item_by_field(self, pk=None, field=None, value=None):
        if not pk or not field or not value:
            raise ValueError('pk, field, value should not None.')

        timeline_class = self.get_timeline_class()
        kwargs = dict()
        kwargs[self.pk] = pk
        kwargs['items__' + field] = value

        timeline = timeline_class.objects(**kwargs).first()

        if timeline is not None:
            for item in timeline.items:
                if item[field] == value:
                    return item

        return None


class TimelineImpl(AbstractTimelineImpl):
    def get_timeline_class(self):
        return Timeline

    def get_item_class(self):
        return TimelineItem

    def validate(self, **kwargs):
        return True

    def all_ids(self, **kwargs):
        """

        :param id:
        :param user_id:
        :param max_id:
        :param min_id:
        :param limit:
        :return:
        """
        items = self.get_items(**kwargs)
        return [item['item_id'] for item in items]

    def items(self, **kwargs):
        return self.get_items(**kwargs)

    def distribute(self, user_id, post):
        # 작성자의 타임라인에 배포
        self._distribute_post(user_id, post['post_id'], type='sent')

    def undistribute(self, user_id, target, post):
        Logger.debug('undistribute 1')
        # 작성자의 타임라인에서 삭제
        self._undistribute_post(user_id, post.post_id)
        Logger.debug('undistribute 2')

    def _distribute_post(self, user_id, post_id, type='post'):
        impl = TimelineImpl()
        try:
            return impl.prepend(pk=user_id, type=type, item_id=post_id)
        except Exception as e:
            Logger.debug(str(e))

    def _undistribute_post(self, user_id, post_id):
        try:
            return self.delete_by_item_id(pk=user_id, item_id=post_id)
        except Exception as e:
            Logger.debug(str(e))
