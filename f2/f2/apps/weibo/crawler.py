"""
微博平台爬虫
Weibo Crawler - 继承 BaseCrawler
"""

import json
from typing import Optional, Dict, Any

from f2.crawlers.base_crawler import BaseCrawler
from f2.apps.weibo.api import WeiboAPIEndpoints
from f2.apps.weibo.model import (
    UserInfoRequest,
    UserTimelineRequest,
    StatusDetailRequest,
    SearchRequest,
)
from f2.apps.weibo.utils import (
    signature_manager,
    ClientConfManager,
)


class WeiboCrawler(BaseCrawler):
    def __init__(self, kwargs: dict = None):
        self.kwargs = kwargs or {}
        proxies = self.kwargs.get("proxies", {"http": None, "https": None})
        cookie = self.kwargs.get("cookie", "")
        self.headers = ClientConfManager.get_headers(cookie)
        super().__init__(self.kwargs, proxies=proxies, crawler_headers=self.headers)

    def fetch_user_info(
        self,
        params: UserInfoRequest
    ) -> dict:
        api = WeiboAPIEndpoints.USER_INFO
        endpoint = f"{api}?type=uid&value={params.uid}"
        
        headers = self.headers.copy()
        return self._fetch_get_json(endpoint, headers=headers)

    def fetch_user_timeline(
        self,
        params: UserTimelineRequest
    ) -> dict:
        api = WeiboAPIEndpoints.USER_TIMELINE
        
        query_params = {
            "type": "uid",
            "value": params.uid,
            "page": params.page,
        }
        
        import urllib.parse
        query_str = urllib.parse.urlencode(query_params)
        endpoint = f"{api}?{query_str}"
        
        headers = self.headers.copy()
        return self._fetch_get_json(endpoint, headers=headers)

    def fetch_status_detail(
        self,
        params: StatusDetailRequest
    ) -> dict:
        api = WeiboAPIEndpoints.STATUS_DETAIL
        endpoint = f"{api}?id={params.id}"
        
        headers = self.headers.copy()
        return self._fetch_get_json(endpoint, headers=headers)

    def fetch_search(
        self,
        params: SearchRequest
    ) -> dict:
        api = WeiboAPIEndpoints.SEARCH
        
        query_params = {
            "containerid": f"100103type=1&q={params.keyword}",
            "page": params.page,
        }
        
        import urllib.parse
        query_str = urllib.parse.urlencode(query_params)
        endpoint = f"{api}?{query_str}"
        
        headers = self.headers.copy()
        return self._fetch_get_json(endpoint, headers=headers)

    def _fetch_get_json(
        self,
        url: str,
        headers: dict = None
    ) -> dict:
        try:
            response = self.get_fetch_data(url)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _fetch_post_json(
        self,
        url: str,
        headers: dict = None,
        data: str = None
    ) -> dict:
        try:
            response = self.post_fetch_data(url, data=data)
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}