"""
TikHub API 包装类 - 抖音数据接口
TikHub API Wrapper for Douyin
"""

import json
import requests
from typing import Optional, Dict, Any, List
from f2.log.logger import logger


class TikHubDouyinAPI:
    """TikHub 抖音 API 客户端"""
    
    DOMAIN_CN = "https://api.tikhub.dev"
    DOMAIN_GLOBAL = "https://api.tikhub.io"
    
    def __init__(self, api_key: str, is_cn_user: bool = True):
        """
        初始化 TikHub API 客户端

        Args:
            api_key: TikHub API Key
            is_cn_user: 是否为中国大陆用户
        """
        self.api_key = api_key
        self.base_url = self.DOMAIN_CN if is_cn_user else self.DOMAIN_GLOBAL
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        self.timeout = 20  # 增加到20秒

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """发送请求"""
        url = f"{self.base_url}{endpoint}"

        timeout_seconds = kwargs.pop('timeout', self.timeout)

        try:
            response = requests.request(
                method,
                url,
                headers=self.headers,
                timeout=timeout_seconds,
                **kwargs
            )

            response.raise_for_status()

            if response.content:
                return response.json()
            return {"success": True}

        except requests.exceptions.Timeout:
            logger.error(f"TikHub API 请求超时: {endpoint}")
            return {"success": False, "error": "API请求超时，请重试"}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"TikHub API 连接失败: {str(e)}")
            return {"success": False, "error": "API连接失败，请检查网络"}
        except requests.exceptions.RequestException as e:
            logger.error(f"TikHub API 请求失败: {str(e)}")
            try:
                if response.content:
                    return response.json()
            except:
                pass
            return {"success": False, "error": str(e)}
    
    def fetch_video_detail(self, aweme_id: str) -> dict:
        """获取视频详情"""
        endpoint = f"/api/v1/douyin/web/fetch_one_video"
        params = {"aweme_id": aweme_id}
        return self._request("GET", endpoint, params=params)
    
    def fetch_video_detail_by_url(self, url: str) -> dict:
        """根据分享链接获取视频详情"""
        endpoint = f"/api/v1/douyin/web/fetch_one_video_by_share_url"
        params = {"share_url": url}
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_profile(self, user_id: str) -> dict:
        """获取用户信息"""
        endpoint = f"/api/v1/douyin/web/fetch_user_info"
        params = {"user_id": user_id}
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_profile_by_url(self, url: str) -> dict:
        """根据用户主页链接获取用户信息"""
        endpoint = f"/api/v1/douyin/web/fetch_user_info_by_url"
        params = {"url": url}
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_posted(self, user_id: str, count: int = 20, max_cursor: int = 0) -> dict:
        """获取用户发布的视频列表"""
        endpoint = f"/api/v1/douyin/web/fetch_user_posted"
        params = {
            "user_id": user_id,
            "count": count,
            "max_cursor": max_cursor
        }
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_posted_by_url(self, url: str, count: int = 20, max_cursor: int = 0) -> dict:
        """根据用户主页链接获取视频列表"""
        endpoint = f"/api/v1/douyin/web/fetch_user_posted_by_url"
        params = {
            "url": url,
            "count": count,
            "max_cursor": max_cursor
        }
        return self._request("GET", endpoint, params=params)
    
    def search_videos(self, keyword: str, offset: int = 0, count: int = 20) -> dict:
        """搜索视频"""
        endpoint = f"/api/v1/douyin/web/search_item"
        params = {
            "keyword": keyword,
            "offset": offset,
            "count": count
        }
        return self._request("GET", endpoint, params=params)
    
    def fetch_video_high_quality_play_url(self, aweme_id: str) -> dict:
        """获取视频最高画质播放链接"""
        endpoint = f"/api/v1/douyin/web/fetch_video_high_quality_play_url"
        params = {"aweme_id": aweme_id}
        return self._request("GET", endpoint, params=params)
    
    def fetch_multi_video_high_quality_play_url(self, aweme_ids: List[str]) -> dict:
        """批量获取视频最高画质播放链接"""
        endpoint = f"/api/v1/douyin/web/fetch_multi_video_high_quality_play_url"
        data = {"aweme_ids": aweme_ids}
        return self._request("POST", endpoint, data=json.dumps(data))
    
    def fetch_user_following(self, user_id: str, count: int = 20, max_cursor: int = 0) -> dict:
        """获取用户关注列表"""
        endpoint = f"/api/v1/douyin/web/fetch_user_following"
        params = {
            "user_id": user_id,
            "count": count,
            "max_cursor": max_cursor
        }
        return self._request("GET", endpoint, params=params)
    
    def fetch_user_fans(self, user_id: str, count: int = 20, max_cursor: int = 0) -> dict:
        """获取用户粉丝列表"""
        endpoint = f"/api/v1/douyin/web/fetch_user_fans"
        params = {
            "user_id": user_id,
            "count": count,
            "max_cursor": max_cursor
        }
        return self._request("GET", endpoint, params=params)
    
    def fetch_video_comments(self, aweme_id: str, count: int = 20, cursor: str = "") -> dict:
        """获取视频评论"""
        endpoint = f"/api/v1/douyin/web/fetch_video_comments"
        params = {
            "aweme_id": aweme_id,
            "count": count,
            "cursor": cursor
        }
        return self._request("GET", endpoint, params=params)