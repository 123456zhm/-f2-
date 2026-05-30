"""
微博处理器
Weibo Handler - 业务逻辑编排
"""

from typing import List, Optional

from f2.apps.weibo.crawler import WeiboCrawler
from f2.apps.weibo.filter import (
    UserProfileFilter,
    StatusCardFilter,
    UserTimelineFilter,
    SearchFilter,
)
from f2.apps.weibo.model import (
    UserInfoRequest,
    UserTimelineRequest,
    StatusDetailRequest,
    SearchRequest,
)
from f2.apps.weibo.utils import StatusIdFetcher, UserIdFetcher


class WeiboHandler:
    def __init__(self, kwargs: dict = None):
        self.kwargs = kwargs or {}

    def fetch_user_profile(self, user_id: str) -> UserProfileFilter:
        if 'weibo.com' in user_id:
            user_id = UserIdFetcher.get_user_id(user_id)

        crawler = WeiboCrawler(self.kwargs)
        params = UserInfoRequest(uid=user_id)
        response = crawler.fetch_user_info(params)
        return UserProfileFilter(response)

    def fetch_one_status(
        self,
        status_id: str
    ) -> StatusCardFilter:
        if 'weibo.com' in status_id:
            status_id = StatusIdFetcher.get_status_id(status_id)

        crawler = WeiboCrawler(self.kwargs)
        params = StatusDetailRequest(id=status_id)
        response = crawler.fetch_status_detail(params)
        return StatusCardFilter(response)

    def fetch_user_timeline(
        self,
        user_id: str,
        page: int = 1,
        count: int = 20
    ) -> UserTimelineFilter:
        if 'weibo.com' in user_id:
            user_id = UserIdFetcher.get_user_id(user_id)

        crawler = WeiboCrawler(self.kwargs)
        params = UserTimelineRequest(
            uid=user_id,
            page=page,
            count=count
        )
        response = crawler.fetch_user_timeline(params)
        return UserTimelineFilter(response)

    def fetch_all_user_timeline(
        self,
        user_id: str,
        max_statuses: int = 0
    ) -> List[dict]:
        page = 1
        count = 0
        statuses = []

        while True:
            result = self.fetch_user_timeline(user_id, page=page)

            if not result.success:
                break

            for status in result.statuses:
                statuses.append(status)
                count += 1
                if max_statuses > 0 and count >= max_statuses:
                    return statuses

            if not result.has_more:
                break

            page += 1

        return statuses

    def fetch_search(
        self,
        keyword: str,
        page: int = 1,
        count: int = 20
    ) -> SearchFilter:
        crawler = WeiboCrawler(self.kwargs)
        params = SearchRequest(
            keyword=keyword,
            page=page,
            count=count
        )
        response = crawler.fetch_search(params)
        return SearchFilter(response)


def get_status_detail(status_id: str) -> dict:
    handler = WeiboHandler()
    status = handler.fetch_one_status(status_id)
    return status.to_dict()


def get_user_statuses(user_id: str, max_statuses: int = 20) -> List[dict]:
    handler = WeiboHandler()
    return handler.fetch_all_user_timeline(user_id, max_statuses)


def search_statuses(keyword: str, page: int = 1) -> List[dict]:
    handler = WeiboHandler()
    result = handler.fetch_search(keyword, page)
    return result.items