"""
抖音处理器
Douyin Handler - 业务逻辑编排
支持两种数据获取方式:
1. Cookie 模式 - 直接调用抖音 API
2. TikHub 模式 - 通过 TikHub API 获取数据
"""

from typing import List, Optional, AsyncGenerator

from f2.apps.douyin.crawler import DouyinCrawler
from f2.apps.douyin.tikhub_api import TikHubDouyinAPI
from f2.apps.douyin.filter import (
    UserProfileFilter,
    VideoCardFilter,
    UserPostedFilter,
    SearchFilter,
)
from f2.apps.douyin.model import (
    UserInfoRequest,
    UserPostedRequest,
    VideoDetailRequest,
    SearchRequest,
)
from f2.apps.douyin.utils import VideoIdFetcher, UserIdFetcher
from f2.log.logger import logger


class DouyinHandler:
    """抖音处理器"""
    
    MODE_COOKIE = "cookie"
    MODE_TIKHUB = "tikhub"
    
    def __init__(self, kwargs: dict = None):
        """
        初始化处理器
        
        Args:
            kwargs: 配置参数，包含:
                - mode: 模式选择 ("cookie" 或 "tikhub")
                - cookie: 抖音 Cookie (cookie 模式)
                - tikhub_api_key: TikHub API Key (tikhub 模式)
                - tikhub_is_cn_user: 是否为中国大陆用户 (默认 True)
        """
        self.kwargs = kwargs or {}
        self.mode = self.kwargs.get("mode", self.MODE_COOKIE)
        self.tikhub_api = None
        
        if self.mode == self.MODE_TIKHUB:
            api_key = self.kwargs.get("tikhub_api_key", "")
            is_cn_user = self.kwargs.get("tikhub_is_cn_user", True)
            if api_key:
                self.tikhub_api = TikHubDouyinAPI(api_key, is_cn_user)
            else:
                logger.warning("TikHub 模式需要提供 tikhub_api_key")
    
    def _is_tikhub_mode(self) -> bool:
        """判断是否为 TikHub 模式"""
        return self.mode == self.MODE_TIKHUB and self.tikhub_api is not None
    
    async def fetch_user_profile(self, user_id: str) -> UserProfileFilter:
        """获取用户信息"""
        if 'douyin.com' in user_id:
            user_id = UserIdFetcher.get_user_id(user_id)
        
        if self._is_tikhub_mode():
            response = self.tikhub_api.fetch_user_profile(user_id)
            return UserProfileFilter(response)
        else:
            async with DouyinCrawler(self.kwargs) as crawler:
                params = UserInfoRequest(user_id=user_id)
                response = await crawler.fetch_user_info(params)
                return UserProfileFilter(response)
    
    async def fetch_one_video(
        self,
        video_id: str
    ) -> VideoCardFilter:
        """获取单个视频详情"""
        is_url = 'douyin.com' in video_id
        
        if is_url:
            original_url = video_id
            video_id = VideoIdFetcher.get_video_id(video_id)
        else:
            original_url = ""
        
        if self._is_tikhub_mode():
            if original_url:
                response = self.tikhub_api.fetch_video_detail_by_url(original_url)
            else:
                response = self.tikhub_api.fetch_video_detail(video_id)
            
            aweme_detail = response.get('data', {}).get('aweme_detail', {})
            return VideoCardFilter(aweme_detail)
        else:
            async with DouyinCrawler(self.kwargs) as crawler:
                params = VideoDetailRequest(aweme_id=video_id)
                response = await crawler.fetch_video_detail(params)
                aweme_detail = response.get('aweme_detail', {})
                return VideoCardFilter(aweme_detail)
    
    async def fetch_user_posted(
        self,
        user_id: str,
        count: int = 20,
        max_cursor: int = 0
    ) -> UserPostedFilter:
        """获取用户发布的视频列表"""
        is_url = 'douyin.com' in user_id
        
        if is_url:
            original_url = user_id
            user_id = UserIdFetcher.get_user_id(user_id)
        else:
            original_url = ""
        
        if self._is_tikhub_mode():
            if original_url:
                response = self.tikhub_api.fetch_user_posted_by_url(
                    original_url, count=count, max_cursor=max_cursor
                )
            else:
                response = self.tikhub_api.fetch_user_posted(
                    user_id, count=count, max_cursor=max_cursor
                )
            return UserPostedFilter(response)
        else:
            async with DouyinCrawler(self.kwargs) as crawler:
                params = UserPostedRequest(
                    user_id=user_id,
                    count=count,
                    max_cursor=max_cursor
                )
                response = await crawler.fetch_user_posted(params)
                return UserPostedFilter(response)
    
    async def fetch_all_user_posted(
        self,
        user_id: str,
        max_videos: int = 0
    ) -> AsyncGenerator[VideoCardFilter, None]:
        """获取用户所有发布的视频"""
        max_cursor = 0
        count = 0
        
        while True:
            result = await self.fetch_user_posted(
                user_id,
                max_cursor=max_cursor
            )
            
            if not result.success:
                break
            
            for video in result.videos:
                yield VideoCardFilter(video)
                count += 1
                if max_videos > 0 and count >= max_videos:
                    return
            
            if not result.has_more:
                break
            
            max_cursor = result.max_cursor
    
    async def fetch_search(
        self,
        keyword: str,
        offset: int = 0,
        count: int = 20
    ) -> SearchFilter:
        """搜索视频"""
        if self._is_tikhub_mode():
            response = self.tikhub_api.search_videos(keyword, offset=offset, count=count)
            return SearchFilter(response)
        else:
            async with DouyinCrawler(self.kwargs) as crawler:
                params = SearchRequest(
                    keyword=keyword,
                    offset=offset,
                    count=count
                )
                response = await crawler.fetch_search(params)
                return SearchFilter(response)


async def get_video_detail(video_id: str) -> dict:
    """获取视频详情 (便捷函数，使用 cookie 模式)"""
    handler = DouyinHandler()
    video = await handler.fetch_one_video(video_id)
    return video.to_dict()


async def get_user_videos(user_id: str, max_videos: int = 20) -> List[dict]:
    """获取用户视频列表 (便捷函数，使用 cookie 模式)"""
    handler = DouyinHandler()
    videos = []
    async for video in handler.fetch_all_user_posted(user_id, max_videos):
        videos.append(video.to_dict())
    return videos


async def search_videos(keyword: str, offset: int = 0) -> List[dict]:
    """搜索视频 (便捷函数，使用 cookie 模式)"""
    handler = DouyinHandler()
    result = await handler.fetch_search(keyword, offset)
    return result.items


async def get_video_detail_tikhub(video_id: str, api_key: str) -> dict:
    """使用 TikHub API 获取视频详情 (便捷函数)"""
    handler = DouyinHandler({
        "mode": DouyinHandler.MODE_TIKHUB,
        "tikhub_api_key": api_key
    })
    video = await handler.fetch_one_video(video_id)
    return video.to_dict()


async def get_user_videos_tikhub(user_id: str, api_key: str, max_videos: int = 20) -> List[dict]:
    """使用 TikHub API 获取用户视频列表 (便捷函数)"""
    handler = DouyinHandler({
        "mode": DouyinHandler.MODE_TIKHUB,
        "tikhub_api_key": api_key
    })
    videos = []
    async for video in handler.fetch_all_user_posted(user_id, max_videos):
        videos.append(video.to_dict())
    return videos


async def search_videos_tikhub(keyword: str, api_key: str, offset: int = 0) -> List[dict]:
    """使用 TikHub API 搜索视频 (便捷函数)"""
    handler = DouyinHandler({
        "mode": DouyinHandler.MODE_TIKHUB,
        "tikhub_api_key": api_key
    })
    result = await handler.fetch_search(keyword, offset)
    return result.items