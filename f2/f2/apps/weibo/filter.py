"""
微博数据过滤器
Weibo Data Filter
"""

import re
from typing import List


class UserProfileFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('data', {})
        self._user = self._data.get('userInfo', {})

    @property
    def user_id(self) -> str:
        return str(self._user.get('id', ''))

    @property
    def nickname(self) -> str:
        return self._user.get('screen_name', '')

    @property
    def avatar(self) -> str:
        return self._user.get('profile_image_url', '')

    @property
    def desc(self) -> str:
        return self._user.get('description', '')

    @property
    def followers_count(self) -> int:
        return self._user.get('followers_count', 0)

    @property
    def following_count(self) -> int:
        return self._user.get('follow_count', 0)

    @property
    def statuses_count(self) -> int:
        return self._user.get('statuses_count', 0)

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'desc': self.desc,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'statuses_count': self.statuses_count,
        }


class StatusCardFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data

    @property
    def status_id(self) -> str:
        return self._data.get('idstr', '') or str(self._data.get('id', ''))

    @property
    def title(self) -> str:
        text = self._data.get('text', '')[:50]
        text = re.sub(r'<[^>]*>', '', text)
        return text

    @property
    def desc(self) -> str:
        text = self._data.get('text', '')
        text = re.sub(r'<[^>]*>', '', text)
        return text

    @property
    def publish_time(self) -> str:
        return self._data.get('created_at', '')

    @property
    def user_id(self) -> str:
        user = self._data.get('user', {})
        return str(user.get('id', ''))

    @property
    def nickname(self) -> str:
        user = self._data.get('user', {})
        return user.get('screen_name', '')

    @property
    def image_list(self) -> List[dict]:
        pics = self._data.get('pic_urls', [])
        result = []
        for pic in pics:
            url = pic.get('url', '')
            if url:
                result.append({
                    'url': url.replace('thumbnail', 'large'),
                    'width': 0,
                    'height': 0,
                })
        return result

    @property
    def video_url(self) -> str:
        page_info = self._data.get('page_info', {})
        return page_info.get('media_info', {}).get('mp4_hd_url', '')

    @property
    def liked_count(self) -> int:
        return self._data.get('attitudes_count', 0)

    @property
    def comment_count(self) -> int:
        return self._data.get('comments_count', 0)

    @property
    def share_count(self) -> int:
        return self._data.get('reposts_count', 0)

    def to_dict(self) -> dict:
        return {
            'status_id': self.status_id,
            'title': self.title,
            'desc': self.desc,
            'publish_time': self.publish_time,
            'user_id': self.user_id,
            'nickname': self.nickname,
            'image_list': self.image_list,
            'video_url': self.video_url,
            'liked_count': self.liked_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count,
        }


class UserTimelineFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('data', {})
        self._cards = self._data.get('cards', [])

    @property
    def success(self) -> bool:
        return self.raw.get('ok', 0) == 1

    @property
    def has_more(self) -> bool:
        return self._data.get('cardlistInfo', {}).get('has_more', False)

    @property
    def statuses(self) -> List[dict]:
        result = []
        for card in self._cards:
            if card.get('card_type') == 9:
                mblog = card.get('mblog', {})
                result.append(StatusCardFilter(mblog).to_dict())
        return result

    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'has_more': self.has_more,
            'statuses': self.statuses,
        }


class SearchFilter:
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('data', {})
        self._cards = self._data.get('cards', [])

    @property
    def success(self) -> bool:
        return self.raw.get('ok', 0) == 1

    @property
    def has_more(self) -> bool:
        return self._data.get('cardlistInfo', {}).get('has_more', False)

    @property
    def total_number(self) -> int:
        return self._data.get('cardlistInfo', {}).get('total_number', 0)

    @property
    def items(self) -> List[dict]:
        result = []
        for card in self._cards:
            if card.get('card_type') == 9:
                mblog = card.get('mblog', {})
                result.append(StatusCardFilter(mblog).to_dict())
        return result

    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'has_more': self.has_more,
            'total_number': self.total_number,
            'items': self.items,
        }