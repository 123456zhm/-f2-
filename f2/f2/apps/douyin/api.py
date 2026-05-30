"""
抖音平台 API 端点定义
Douyin / TikTok API Endpoints
"""

class DouyinAPIEndpoints:
    DOMAIN = "https://www.douyin.com"
    WEB_DOMAIN = "https://www.douyin.com"
    
    USER_INFO = f"{DOMAIN}/aweme/v1/user/"
    USER_POSTED = f"{DOMAIN}/aweme/v1/user/post/"
    VIDEO_DETAIL = f"{DOMAIN}/aweme/v1/web/aweme/detail/"
    SEARCH = f"{DOMAIN}/aweme/v1/web/search/item/"
    FEED = f"{DOMAIN}/aweme/v1/feed/"
    FOLLOWING = f"{DOMAIN}/aweme/v1/user/following/list/"
    FANS = f"{DOMAIN}/aweme/v1/user/follower/list/"


class DouyinHeaders:
    DEFAULT = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.douyin.com",
        "pragma": "no-cache",
        "referer": "https://www.douyin.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }