"""
小红书平台爬虫
Xiaohongshu Crawler - 继承 BaseCrawler
"""

import asyncio
import json
from typing import Optional, Dict, Any

from f2.crawlers.base_crawler import BaseCrawler
from f2.apps.xiaohongshu.api import XiaohongshuAPIEndpoints
from f2.apps.xiaohongshu.model import (
    UserProfileRequest,
    UserPostedRequest,
    NoteDetailRequest,
    SearchNotesRequest,
)
from f2.apps.xiaohongshu.utils import (
    signature_manager,
    ClientConfManager,
)


class XiaohongshuCrawler(BaseCrawler):
    """小红书爬虫"""
    
    def __init__(self, kwargs: dict = None):
        """
        初始化爬虫
        
        Args:
            kwargs: 配置参数，包含 cookie, proxies 等
        """
        self.kwargs = kwargs or {}
        
        proxies = self.kwargs.get("proxies", {"http": None, "https": None})
        
        cookie = self.kwargs.get("cookie", "")
        self.headers = ClientConfManager.get_headers(cookie)
        
        self.a1 = self._extract_a1(cookie)
        
        super().__init__(self.kwargs, proxies=proxies, crawler_headers=self.headers)
    
    def _extract_a1(self, cookie: str) -> str:
        """从 Cookie 中提取 a1 值"""
        if not cookie:
            return ""
        
        for item in cookie.split(';'):
            item = item.strip()
            if item.startswith('a1='):
                return item[3:]
        return ""
    
    def _add_sign(self, api: str, data: Optional[dict] = None) -> dict:
        """添加签名到请求头"""
        sign = signature_manager.generate_sign(api, data, self.a1)
        return sign
    
    def fetch_user_profile(
        self, 
        params: UserProfileRequest
    ) -> dict:
        """
        获取用户信息
        
        Args:
            params: 用户信息请求参数
            
        Returns:
            用户信息 JSON
        """
        api = XiaohongshuAPIEndpoints.USER_PROFILE
        endpoint = f"{api}?user_id={params.user_id}"
        
        sign = self._add_sign(f"/api/sns/web/v1/user?user_id={params.user_id}")
        headers = self.headers.copy()
        headers.update(sign)
        
        return self._fetch_get_json(endpoint, headers=headers)
    
    def fetch_user_posted(
        self, 
        params: UserPostedRequest
    ) -> dict:
        """
        获取用户发布的笔记列表
        
        Args:
            params: 用户笔记列表请求参数
            
        Returns:
            笔记列表 JSON
        """
        api = XiaohongshuAPIEndpoints.USER_POSTED
        
        query_params = {
            "num": params.num,
            "cursor": params.cursor,
            "user_id": params.user_id,
            "image_formats": params.image_formats,
            "xsec_token": params.xsec_token,
            "xsec_source": params.xsec_source,
        }
        
        import urllib.parse
        query_str = urllib.parse.urlencode(query_params)
        endpoint = f"{api}?{query_str}"
        
        sign = self._add_sign(f"/api/sns/web/v1/user_posted?{query_str}")
        headers = self.headers.copy()
        headers.update(sign)
        
        return self._fetch_get_json(endpoint, headers=headers)
    
    def fetch_note_detail(
        self, 
        params: NoteDetailRequest
    ) -> dict:
        """
        获取笔记详情
        
        Args:
            params: 笔记详情请求参数
            
        Returns:
            笔记详情 JSON
        """
        api = XiaohongshuAPIEndpoints.FEED
        
        data = {
            "source_note_id": params.source_note_id,
            "image_formats": params.image_formats.split(','),
            "extra": params.extra,
            "xsec_source": params.xsec_source,
            "xsec_token": params.xsec_token,
        }
        
        sign = self._add_sign("/api/sns/web/v1/feed", data)
        headers = self.headers.copy()
        headers.update(sign)
        
        return self._fetch_post_json(
            api, 
            headers=headers, 
            data=json.dumps(data, separators=(',', ':'))
        )
    
    def fetch_search_notes(
        self, 
        params: SearchNotesRequest
    ) -> dict:
        """
        搜索笔记
        
        Args:
            params: 搜索请求参数
            
        Returns:
            搜索结果 JSON
        """
        api = XiaohongshuAPIEndpoints.SEARCH_NOTES
        
        query_params = {
            "keyword": params.keyword,
            "page": params.page,
            "page_size": params.page_size,
            "search_type": params.search_type,
        }
        
        import urllib.parse
        query_str = urllib.parse.urlencode(query_params)
        endpoint = f"{api}?{query_str}"
        
        sign = self._add_sign(f"/api/sns/web/v1/search/notes?{query_str}")
        headers = self.headers.copy()
        headers.update(sign)
        
        return self._fetch_get_json(endpoint, headers=headers)
    
    async def _async_fetch_get_json(
        self, 
        url: str, 
        headers: dict = None
    ) -> dict:
        """异步发送 GET 请求并返回 JSON"""
        try:
            if self.session is None:
                await self._create_session()
            response = await self.get_fetch_data(url)
            text = await response.text()
            if response.status != 200:
                return {"success": False, "error": f"HTTP {response.status}: {text[:300]}"}
            return json.loads(text) if text else {}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await self._close_session()
    
    async def _async_fetch_post_json(
        self, 
        url: str, 
        headers: dict = None,
        data: str = None
    ) -> dict:
        """异步发送 POST 请求并返回 JSON"""
        try:
            if self.session is None:
                await self._create_session()
            response = await self.post_fetch_data(url, data=data)
            text = await response.text()
            if response.status != 200:
                return {"success": False, "error": f"HTTP {response.status}: {text[:300]}"}
            return json.loads(text) if text else {}
        except Exception as e:
            return {"success": False, "error": str(e)}
        finally:
            await self._close_session()
    
    def _fetch_get_json(
        self, 
        url: str, 
        headers: dict = None
    ) -> dict:
        """发送 GET 请求并返回 JSON（同步包装）"""
        try:
            return asyncio.run(self._async_fetch_get_json(url, headers))
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _fetch_post_json(
        self, 
        url: str, 
        headers: dict = None,
        data: str = None
    ) -> dict:
        """发送 POST 请求并返回 JSON（同步包装）"""
        try:
            return asyncio.run(self._async_fetch_post_json(url, headers, data))
        except Exception as e:
            return {"success": False, "error": str(e)}