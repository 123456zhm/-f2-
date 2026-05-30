"""
小红书处理器
Xiaohongshu Handler - 业务逻辑编排
支持两种数据获取方式:
1. Cookie 模式 - 直接调用小红书 API
2. TikHub 模式 - 通过 TikHub API 获取数据
"""

from typing import List, Optional

from f2.apps.xiaohongshu.crawler import XiaohongshuCrawler
from f2.apps.xiaohongshu.tikhub_api import TikHubXiaohongshuAPI
from f2.apps.xiaohongshu.filter import (
    UserProfileFilter,
    NoteCardFilter,
    UserPostedFilter,
    SearchFilter,
)
from f2.apps.xiaohongshu.model import (
    UserProfileRequest,
    UserPostedRequest,
    NoteDetailRequest,
    SearchNotesRequest,
)
from f2.apps.xiaohongshu.utils import NoteIdFetcher, UserIdFetcher
from f2.log.logger import logger


class XiaohongshuHandler:
    """小红书处理器"""
    
    # 支持的模式
    MODE_COOKIE = "cookie"
    MODE_TIKHUB = "tikhub"
    
    def __init__(self, kwargs: dict = None):
        """
        初始化处理器
        
        Args:
            kwargs: 配置参数，包含:
                - mode: 模式选择 ("cookie" 或 "tikhub")
                - cookie: 小红书 Cookie (cookie 模式)
                - tikhub_api_key: TikHub API Key (tikhub 模式)
                - tikhub_is_cn_user: 是否为中国大陆用户 (默认 True)
        """
        self.kwargs = kwargs or {}
        self.mode = self.kwargs.get("mode", self.MODE_COOKIE)
        self.tikhub_api = None
        
        # 如果是 TikHub 模式，初始化 API 客户端
        if self.mode == self.MODE_TIKHUB:
            api_key = self.kwargs.get("tikhub_api_key", "")
            is_cn_user = self.kwargs.get("tikhub_is_cn_user", True)
            if api_key:
                self.tikhub_api = TikHubXiaohongshuAPI(api_key, is_cn_user)
            else:
                logger.warning("TikHub 模式需要提供 tikhub_api_key")
    
    def _is_tikhub_mode(self) -> bool:
        """判断是否为 TikHub 模式"""
        return self.mode == self.MODE_TIKHUB and self.tikhub_api is not None
    
    def fetch_user_profile(self, user_id: str) -> UserProfileFilter:
        """
        获取用户信息
        
        Args:
            user_id: 用户 ID 或用户主页 URL
            
        Returns:
            UserProfileFilter
        """
        if 'xiaohongshu.com' in user_id:
            user_id = UserIdFetcher.get_user_id(user_id)
        
        if self._is_tikhub_mode():
            response = self.tikhub_api.fetch_user_profile(user_id)
            return UserProfileFilter(response)
        else:
            crawler = XiaohongshuCrawler(self.kwargs)
            params = UserProfileRequest(user_id=user_id)
            response = crawler.fetch_user_profile(params)
            return UserProfileFilter(response)
    
    def fetch_one_note(
        self, 
        note_id: str, 
        xsec_token: str = ""
    ) -> NoteCardFilter:
        """
        获取单个笔记详情
        
        Args:
            note_id: 笔记 ID 或笔记 URL
            xsec_token: 安全令牌 (cookie 模式使用)
            
        Returns:
            NoteCardFilter
        """
        is_url = 'xiaohongshu.com' in note_id or 'xhslink.com' in note_id
        
        if is_url:
            original_url = note_id
            # 从 URL 中提取 xsec_token（短链接会先解析获取真实URL）
            if 'xhslink.com' in note_id:
                extracted_token = NoteIdFetcher.get_xsec_token(note_id)
                if extracted_token:
                    xsec_token = extracted_token
            note_id = NoteIdFetcher.get_note_id(note_id)
        else:
            original_url = ""
        
        if not note_id:
            return NoteCardFilter({})
        
        if self._is_tikhub_mode():
            # TikHub 模式：优先使用 URL 获取
            if original_url:
                response = self.tikhub_api.fetch_note_detail_by_url(original_url)
            else:
                response = self.tikhub_api.fetch_note_detail(note_id)
            
            items = response.get('data', {}).get('items', [])
            if items:
                return NoteCardFilter(items[0], xsec_token)
            return NoteCardFilter({})
        else:
            cookie = self.kwargs.get("cookie", "")
            
            # 方案1：尝试 API 调用
            crawler = XiaohongshuCrawler(self.kwargs)
            params = NoteDetailRequest(
                source_note_id=note_id,
                xsec_token=xsec_token
            )
            response = crawler.fetch_note_detail(params)
            
            items = response.get('data', {}).get('items', [])
            if items:
                return NoteCardFilter(items[0], xsec_token)
            
            # 方案2：API 失败(如签名过期)，回退到网页解析
            if response.get('success') is False:
                logger.info("API 请求失败，尝试网页解析回退...")
                web_data = NoteIdFetcher.fetch_note_from_web(
                    original_url or f"https://www.xiaohongshu.com/explore/{note_id}",
                    cookie=cookie
                )
                if web_data:
                    return NoteCardFilter(web_data, xsec_token)
            
            return NoteCardFilter({})
    
    def fetch_user_posted(
        self, 
        user_id: str,
        num: int = 30,
        cursor: str = "",
        xsec_token: str = ""
    ) -> UserPostedFilter:
        """
        获取用户发布的笔记列表
        
        Args:
            user_id: 用户 ID 或用户主页 URL
            num: 每页数量
            cursor: 分页游标
            xsec_token: 安全令牌 (cookie 模式使用)
            
        Returns:
            UserPostedFilter
        """
        is_url = 'xiaohongshu.com' in user_id
        
        if is_url:
            original_url = user_id
            user_id = UserIdFetcher.get_user_id(user_id)
        else:
            original_url = ""
        
        if self._is_tikhub_mode():
            # TikHub 模式：优先使用 URL 获取
            if original_url:
                response = self.tikhub_api.fetch_user_posted_by_url(
                    original_url, num=num, cursor=cursor
                )
            else:
                response = self.tikhub_api.fetch_user_posted(
                    user_id, num=num, cursor=cursor
                )
            return UserPostedFilter(response)
        else:
            crawler = XiaohongshuCrawler(self.kwargs)
            params = UserPostedRequest(
                user_id=user_id,
                num=num,
                cursor=cursor,
                xsec_token=xsec_token
            )
            response = crawler.fetch_user_posted(params)
            return UserPostedFilter(response)
    
    def fetch_all_user_posted(
        self, 
        user_id: str,
        max_notes: int = 0
    ) -> List[dict]:
        """
        获取用户所有发布的笔记
        
        Args:
            user_id: 用户 ID 或用户主页 URL
            max_notes: 最大数量 (0 不限制)
            
        Returns:
            笔记列表
        """
        cursor = ""
        xsec_token = ""
        count = 0
        notes = []
        
        while True:
            result = self.fetch_user_posted(
                user_id, 
                cursor=cursor, 
                xsec_token=xsec_token
            )
            
            if not result.success:
                break
            
            for note in result.notes:
                notes.append(note)
                count += 1
                if max_notes > 0 and count >= max_notes:
                    return notes
            
            if not result.has_more:
                break
            
            cursor = result.cursor
        
        return notes
    
    def fetch_search(
        self, 
        keyword: str,
        page: int = 1,
        page_size: int = 20
    ) -> SearchFilter:
        """
        搜索笔记
        
        Args:
            keyword: 搜索关键词
            page: 页码
            page_size: 每页数量
            
        Returns:
            SearchFilter
        """
        if self._is_tikhub_mode():
            response = self.tikhub_api.search_notes(keyword, page=page, page_size=page_size)
            return SearchFilter(response)
        else:
            crawler = XiaohongshuCrawler(self.kwargs)
            params = SearchNotesRequest(
                keyword=keyword,
                page=page,
                page_size=page_size
            )
            response = crawler.fetch_search_notes(params)
            return SearchFilter(response)


def get_note_detail(note_id: str, xsec_token: str = "") -> dict:
    """获取笔记详情 (便捷函数，使用 cookie 模式)"""
    handler = XiaohongshuHandler()
    note = handler.fetch_one_note(note_id, xsec_token)
    return note.to_dict()


def get_user_notes(user_id: str, max_notes: int = 30) -> List[dict]:
    """获取用户笔记列表 (便捷函数，使用 cookie 模式)"""
    handler = XiaohongshuHandler()
    return handler.fetch_all_user_posted(user_id, max_notes)


def search_notes(keyword: str, page: int = 1) -> List[dict]:
    """搜索笔记 (便捷函数，使用 cookie 模式)"""
    handler = XiaohongshuHandler()
    result = handler.fetch_search(keyword, page)
    return result.items


def get_note_detail_tikhub(note_id: str, api_key: str) -> dict:
    """使用 TikHub API 获取笔记详情 (便捷函数)"""
    handler = XiaohongshuHandler({
        "mode": XiaohongshuHandler.MODE_TIKHUB,
        "tikhub_api_key": api_key
    })
    note = handler.fetch_one_note(note_id)
    return note.to_dict()


def get_user_notes_tikhub(user_id: str, api_key: str, max_notes: int = 30) -> List[dict]:
    """使用 TikHub API 获取用户笔记列表 (便捷函数)"""
    handler = XiaohongshuHandler({
        "mode": XiaohongshuHandler.MODE_TIKHUB,
        "tikhub_api_key": api_key
    })
    return handler.fetch_all_user_posted(user_id, max_notes)


def search_notes_tikhub(keyword: str, api_key: str, page: int = 1) -> List[dict]:
    """使用 TikHub API 搜索笔记 (便捷函数)"""
    handler = XiaohongshuHandler({
        "mode": XiaohongshuHandler.MODE_TIKHUB,
        "tikhub_api_key": api_key
    })
    result = handler.fetch_search(keyword, page)
    return result.items