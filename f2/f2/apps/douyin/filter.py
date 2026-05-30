"""
抖音数据过滤器
Douyin Data Filter
"""

import re
from typing import List
from datetime import datetime


class UserProfileFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('user', {})

    @property
    def user_id(self) -> str:
        return self._data.get('uid', '') or self._data.get('user_id', '')

    @property
    def nickname(self) -> str:
        return self._data.get('nickname', '')

    @property
    def avatar(self) -> str:
        avatar_list = self._data.get('avatar_thumb', {}).get('url_list', [])
        return avatar_list[0] if avatar_list else ''

    @property
    def desc(self) -> str:
        return self._data.get('signature', '')

    @property
    def follower_count(self) -> int:
        return self._data.get('follower_count', 0)

    @property
    def following_count(self) -> int:
        return self._data.get('following_count', 0)

    @property
    def total_favorited(self) -> int:
        return self._data.get('total_favorited', 0)

    @property
    def aweme_count(self) -> int:
        return self._data.get('aweme_count', 0)

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'desc': self.desc,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'total_favorited': self.total_favorited,
            'aweme_count': self.aweme_count,
        }


class VideoCardFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data

    @property
    def aweme_id(self) -> str:
        return self._data.get('aweme_id', '')

    @property
    def title(self) -> str:
        return self._data.get('desc', '')[:50]

    @property
    def desc(self) -> str:
        return self._data.get('desc', '')

    @property
    def publish_time(self) -> str:
        timestamp = self._data.get('create_time', 0)
        if timestamp:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return ''

    @property
    def user_id(self) -> str:
        user = self._data.get('author', {})
        return user.get('uid', '') or user.get('user_id', '')

    @property
    def nickname(self) -> str:
        user = self._data.get('author', {})
        return user.get('nickname', '')

    @property
    def video_url(self) -> str:
        video = self._data.get('video', {})
        play_addr = video.get('play_addr', {})
        url_list = play_addr.get('url_list', [])
        return url_list[0] if url_list else ''

    @property
    def cover_url(self) -> str:
        video = self._data.get('video', {})
        cover = video.get('cover', {})
        url_list = cover.get('url_list', [])
        return url_list[0] if url_list else ''

    @property
    def liked_count(self) -> int:
        stats = self._data.get('statistics', {})
        return stats.get('digg_count', 0)

    @property
    def comment_count(self) -> int:
        stats = self._data.get('statistics', {})
        return stats.get('comment_count', 0)

    @property
    def share_count(self) -> int:
        stats = self._data.get('statistics', {})
        return stats.get('share_count', 0)

    @property
    def collected_count(self) -> int:
        stats = self._data.get('statistics', {})
        return stats.get('collect_count', 0)

    def to_dict(self) -> dict:
        return {
            'aweme_id': self.aweme_id,
            'title': self.title,
            'desc': self.desc,
            'publish_time': self.publish_time,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'video_url': self.video_url,
            'cover_url': self.cover_url,
            'liked_count': self.liked_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count,
            'collected_count': self.collected_count,
        }


class UserPostedFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('aweme_list', [])

    @property
    def success(self) -> bool:
        return self.raw.get('status_code', 0) == 0

    @property
    def has_more(self) -> bool:
        return self.raw.get('has_more', False)

    @property
    def max_cursor(self) -> int:
        return self.raw.get('max_cursor', 0)

    @property
    def videos(self) -> List[dict]:
        return [VideoCardFilter(v).to_dict() for v in self._data]

    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'has_more': self.has_more,
            'max_cursor': self.max_cursor,
            'videos': self.videos,
        }


class SearchFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('data', {}).get('aweme_list', [])

    @property
    def success(self) -> bool:
        return self.raw.get('status_code', 0) == 0

    @property
    def has_more(self) -> bool:
        return self.raw.get('has_more', False)

    @property
    def cursor(self) -> int:
        return self.raw.get('cursor', 0)

    @property
    def items(self) -> List[dict]:
        return [VideoCardFilter(v).to_dict() for v in self._data]

    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'has_more': self.has_more,
            'cursor': self.cursor,
            'items': self.items,
        }