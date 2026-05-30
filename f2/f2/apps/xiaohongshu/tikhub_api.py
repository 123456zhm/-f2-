"""
TikHub API 包装类 - 小红书数据接口
TikHub API Wrapper for Xiaohongshu
"""

import json
import requests
from typing import Optional, Dict, Any, List
from f2.log.logger import logger


class TikHubXiaohongshuAPI:
    """TikHub 小红书 API 客户端"""
    
    # 根据地区选择域名
    DOMAIN_CN = "https://api.tikhub.dev"
    DOMAIN_GLOBAL = "https://api.tikhub.io"
    
    def __init__(self, api_key: str, is_cn_user: bool = True):
        """
        初始化 TikHub API 客户端
        
        Args:
            api_key: TikHub API Key
            is_cn_user: 是否为中国大陆用户（影响域名选择）
        """
        self.api_key = api_key
        self.base_url = self.DOMAIN_CN if is_cn_user else self.DOMAIN_GLOBAL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        self.timeout = 25
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        发送请求
        
        Args:
            method: HTTP 方法 (GET/POST)
            endpoint: API 端点
            **kwargs: 其他请求参数
        
        Returns:
            响应 JSON 数据
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                timeout=self.timeout,
                **kwargs
            )
            
            response.raise_for_status()
            
            if response.content:
                return response.json()
            return {"success": True}
            
        except requests.exceptions.Timeout as e:
            logger.error(f"TikHub API 请求超时: {str(e)}")
            return {"success": False, "error": f"请求超时: {str(e)}"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"TikHub API 请求失败: {str(e)}")
            try:
                if response.content:
                    return response.json()
            except:
                pass
            return {"success": False, "error": str(e)}
    
    def fetch_note_detail(self, note_id: str) -> dict:
        """
        获取笔记详情
        
        Args:
            note_id: 笔记 ID
        
        Returns:
            笔记详情数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_one_note"
        params = {"note_id": note_id}
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_note_detail_by_url(self, url: str) -> dict:
        """
        根据分享链接获取笔记详情
        
        Args:
            url: 笔记分享链接
        
        Returns:
            笔记详情数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_one_note_by_share_url"
        params = {"url": url}
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_profile(self, user_id: str) -> dict:
        """
        获取用户信息
        
        Args:
            user_id: 用户 ID
        
        Returns:
            用户信息数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_user_profile"
        params = {"user_id": user_id}
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_profile_by_url(self, url: str) -> dict:
        """
        根据用户主页链接获取用户信息
        
        Args:
            url: 用户主页链接
        
        Returns:
            用户信息数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_user_profile_by_url"
        params = {"url": url}
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_posted(self, user_id: str, num: int = 30, cursor: str = "") -> dict:
        """
        获取用户发布的笔记列表
        
        Args:
            user_id: 用户 ID
            num: 每页数量
            cursor: 分页游标
        
        Returns:
            用户笔记列表数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_user_posted"
        params = {
            "user_id": user_id,
            "num": num,
            "cursor": cursor
        }
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_posted_by_url(self, url: str, num: int = 30, cursor: str = "") -> dict:
        """
        根据用户主页链接获取用户发布的笔记列表
        
        Args:
            url: 用户主页链接
            num: 每页数量
            cursor: 分页游标
        
        Returns:
            用户笔记列表数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_user_posted_by_url"
        params = {
            "url": url,
            "num": num,
            "cursor": cursor
        }
        
        return self._request("GET", endpoint, params=params)
    
    def search_notes(self, keyword: str, page: int = 1, page_size: int = 20) -> dict:
        """
        搜索笔记
        
        Args:
            keyword: 搜索关键词
            page: 页码
            page_size: 每页数量
        
        Returns:
            搜索结果数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/search_notes"
        params = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size
        }
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_note_high_quality_play_url(self, note_id: str) -> dict:
        """
        获取视频最高画质播放链接
        
        Args:
            note_id: 笔记 ID
        
        Returns:
            视频播放链接数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_note_high_quality_play_url"
        params = {"note_id": note_id}
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_multi_notes(self, note_ids: List[str]) -> dict:
        """
        批量获取笔记信息
        
        Args:
            note_ids: 笔记 ID 列表
        
        Returns:
            笔记信息列表
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_multi_notes"
        data = {"note_ids": note_ids}
        
        return self._request("POST", endpoint, data=json.dumps(data))
    
    def fetch_home_feed(self, page_size: int = 20) -> dict:
        """
        获取首页推荐笔记
        
        Args:
            page_size: 每页数量
        
        Returns:
            首页推荐数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_home_feed"
        params = {"page_size": page_size}
        
        return self._request("GET", endpoint, params=params)
    
    def fetch_note_comments(self, note_id: str, page: int = 1, page_size: int = 20) -> dict:
        """
        获取笔记评论
        
        Args:
            note_id: 笔记 ID
            page: 页码
            page_size: 每页数量
        
        Returns:
            评论列表数据
        """
        endpoint = f"/api/v1/xiaohongshu/web/fetch_note_comments"
        params = {
            "note_id": note_id,
            "page": page,
            "page_size": page_size
        }
        
        return self._request("GET", endpoint, params=params)
