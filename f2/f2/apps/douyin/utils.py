# path: f2/apps/douyin/utils.py

"""
抖音平台工具函数
Douyin Utilities
"""

import re
import time
import hashlib
from typing import Optional, Dict, List


class DouyinSignatureManager:
    def __init__(self):
        pass

    def generate_sign(self, api: str, params: dict = None) -> Dict[str, str]:
        timestamp = int(time.time())
        params_str = "&".join([f"{k}={v}" for k, v in (params or {}).items()])
        sign_str = f"{api}?{params_str}{timestamp}"
        x_sign = hashlib.md5(sign_str.encode()).hexdigest()
        return {
            "x-sign": x_sign,
            "x-t": str(timestamp)
        }


class ClientConfManager:
    DEFAULT_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.douyin.com",
        "referer": "https://www.douyin.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    @classmethod
    def get_headers(cls, cookie: str = "") -> dict:
        headers = cls.DEFAULT_HEADERS.copy()
        if cookie:
            headers["cookie"] = cookie
        return headers


class VideoIdFetcher:
    @staticmethod
    def get_video_id(url: str) -> str:
        match = re.search(r'/video/(\d+)', url)
        if match:
            return match.group(1)
        
        match = re.search(r'/aweme/v1/web/aweme/detail.*?aweme_id=(\d+)', url)
        if match:
            return match.group(1)
        
        match = re.search(r'douyin\.com/(\d+)', url)
        if match:
            return match.group(1)
        
        if re.match(r'^\d{19,}$', url):
            return url
        
        short_id_match = re.search(r'v\.douyin\.com/([a-zA-Z0-9]+)', url)
        if short_id_match:
            return short_id_match.group(1)
        
        return ""
    
    @staticmethod
    def is_short_id(video_id: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9]{10,}$', video_id)) and not video_id.isdigit()

    @staticmethod
    def get_all_video_id(urls: List[str]) -> List[str]:
        return [VideoIdFetcher.get_video_id(url) for url in urls]


class UserIdFetcher:
    @staticmethod
    def get_user_id(url: str) -> str:
        match = re.search(r'/user/(\d+)', url)
        if match:
            return match.group(1)
        
        match = re.search(r'@(\w+)', url)
        if match:
            return match.group(1)
        
        if re.match(r'^\d{19,}$', url):
            return url
        
        return ""

    @staticmethod
    def get_all_user_id(urls: List[str]) -> List[str]:
        return [UserIdFetcher.get_user_id(url) for url in urls]


signature_manager = DouyinSignatureManager()