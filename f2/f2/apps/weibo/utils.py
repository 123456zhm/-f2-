# path: f2/apps/weibo/utils.py

"""
微博平台工具函数
Weibo Utilities
"""

import re
from typing import Optional, Dict, List


class WeiboSignatureManager:
    def __init__(self):
        pass

    def generate_sign(self, api: str, params: dict = None) -> Dict[str, str]:
        return {}


class ClientConfManager:
    DEFAULT_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://m.weibo.cn",
        "referer": "https://m.weibo.cn/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    @classmethod
    def get_headers(cls, cookie: str = "") -> dict:
        headers = cls.DEFAULT_HEADERS.copy()
        if cookie:
            headers["cookie"] = cookie
        return headers


class StatusIdFetcher:
    @staticmethod
    def get_status_id(url: str) -> str:
        match = re.search(r'/status/(\d+)', url)
        if match:
            return match.group(1)
        
        match = re.search(r'weibo\.com/(\d+)/', url)
        if match:
            return match.group(1)
        
        if re.match(r'^\d{16,}$', url):
            return url
        
        return ""

    @staticmethod
    def get_all_status_id(urls: List[str]) -> List[str]:
        return [StatusIdFetcher.get_status_id(url) for url in urls]


class UserIdFetcher:
    @staticmethod
    def get_user_id(url: str) -> str:
        match = re.search(r'/u/(\d+)', url)
        if match:
            return match.group(1)
        
        match = re.search(r'/profile/(\d+)', url)
        if match:
            return match.group(1)
        
        match = re.search(r'weibo\.com/(\d+)', url)
        if match:
            return match.group(1)
        
        if re.match(r'^\d{10,}$', url):
            return url
        
        return ""

    @staticmethod
    def get_all_user_id(urls: List[str]) -> List[str]:
        return [UserIdFetcher.get_user_id(url) for url in urls]


signature_manager = WeiboSignatureManager()