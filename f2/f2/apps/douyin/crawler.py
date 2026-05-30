"""
抖音平台爬虫
Douyin Crawler - 继承 BaseCrawler
"""

import json
import re
import urllib.parse
from typing import Optional, Dict, Any

from f2.crawlers.base_crawler import BaseCrawler
from f2.apps.douyin.api import DouyinAPIEndpoints
from f2.apps.douyin.model import (
    UserInfoRequest,
    UserPostedRequest,
    VideoDetailRequest,
    SearchRequest,
)
from f2.apps.douyin.utils import (
    signature_manager,
    ClientConfManager,
    VideoIdFetcher,
)


class DouyinCrawler(BaseCrawler):
    def __init__(self, kwargs: dict = None):
        self.kwargs = kwargs or {}
        proxies = self.kwargs.get("proxies", {"http://": None, "https://": None})
        cookie = self.kwargs.get("cookie", "")
        self.headers = ClientConfManager.get_headers(cookie)
        super().__init__(self.kwargs, proxies=proxies, crawler_headers=self.headers)

    async def fetch_user_info(
        self,
        params: UserInfoRequest
    ) -> dict:
        api = DouyinAPIEndpoints.USER_INFO
        endpoint = f"{api}?user_id={params.user_id}"
        
        headers = self.headers.copy()
        return await self._fetch_get_json(endpoint, headers=headers)

    async def fetch_user_posted(
        self,
        params: UserPostedRequest
    ) -> dict:
        api = DouyinAPIEndpoints.USER_POSTED
        
        query_params = {
            "user_id": params.user_id,
            "max_cursor": params.max_cursor,
            "count": params.count,
        }
        
        query_str = urllib.parse.urlencode(query_params)
        endpoint = f"{api}?{query_str}"
        
        headers = self.headers.copy()
        return await self._fetch_get_json(endpoint, headers=headers)

    async def _resolve_short_url(self, short_id: str) -> Optional[str]:
        try:
            short_url = f"https://v.douyin.com/{short_id}/"
            async with self.session.get(short_url, allow_redirects=True) as response:
                final_url = str(response.url)
                return final_url
        except Exception as e:
            return None

    async def fetch_video_detail(
        self,
        params: VideoDetailRequest
    ) -> dict:
        aweme_id = params.aweme_id
        
        if VideoIdFetcher.is_short_id(aweme_id):
            resolved_url = await self._resolve_short_url(aweme_id)
            if resolved_url:
                aweme_id = VideoIdFetcher.get_video_id(resolved_url)
                if not aweme_id or VideoIdFetcher.is_short_id(aweme_id):
                    return {"success": False, "error": "无法解析短链接获取视频ID"}
        
        api = DouyinAPIEndpoints.VIDEO_DETAIL
        # 添加 aid 和空的 a_bogus 参数来绕过抖音的反爬签名检查
        endpoint = f"{api}?aweme_id={aweme_id}&aid=6383&a_bogus="
        
        headers = self.headers.copy()
        return await self._fetch_get_json(endpoint, headers=headers)

    async def fetch_search(
        self,
        params: SearchRequest
    ) -> dict:
        api = DouyinAPIEndpoints.SEARCH
        
        query_params = {
            "keyword": params.keyword,
            "offset": params.offset,
            "count": params.count,
            "search_source": params.search_source,
        }
        
        query_str = urllib.parse.urlencode(query_params)
        endpoint = f"{api}?{query_str}"
        
        headers = self.headers.copy()
        return await self._fetch_get_json(endpoint, headers=headers)

    async def _fetch_get_json(
        self,
        url: str,
        headers: dict = None
    ) -> dict:
        response = None
        try:
            response = await self.get_fetch_data(url)
            return await response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if response is not None:
                response.release()

    async def _fetch_post_json(
        self,
        url: str,
        headers: dict = None,
        data: str = None
    ) -> dict:
        response = None
        try:
            response = await self.post_fetch_data(url, data=data)
            return await response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            if response is not None:
                response.release()