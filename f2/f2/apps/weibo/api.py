"""
微博平台 API 端点定义
Weibo API Endpoints
"""

class WeiboAPIEndpoints:
    DOMAIN = "https://m.weibo.cn"
    WEB_DOMAIN = "https://weibo.com"
    
    USER_INFO = f"{DOMAIN}/api/container/getIndex"
    USER_TIMELINE = f"{DOMAIN}/api/container/getIndex"
    STATUS_DETAIL = f"{DOMAIN}/api/statuses/show"
    SEARCH = f"{DOMAIN}/api/container/getIndex"
    COMMENT = f"{DOMAIN}/api/comments/show"


class WeiboHeaders:
    DEFAULT = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://m.weibo.cn",
        "pragma": "no-cache",
        "referer": "https://m.weibo.cn/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }