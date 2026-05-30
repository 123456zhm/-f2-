"""
小红书平台 API 端点定义
Xiaohongshu (Little Red Book) API Endpoints
"""

class XiaohongshuAPIEndpoints:
    """小红书 API 端点"""
    
    # 基础域名
    DOMAIN = "https://edith.xiaohongshu.com"
    WEB_DOMAIN = "https://www.xiaohongshu.com"
    
    # 用户相关接口
    USER_PROFILE = f"{DOMAIN}/api/sns/web/v1/user"  # 用户信息
    USER_POSTED = f"{DOMAIN}/api/sns/web/v1/user_posted"  # 用户发布的笔记
    
    # 笔记相关接口
    FEED = f"{DOMAIN}/api/sns/web/v1/feed"  # 笔记详情
    NOTE_DETAIL = f"{DOMAIN}/api/sns/web/v1/note_detail"  # 笔记详情(备用)
    
    # 搜索相关接口
    SEARCH_NOTES = f"{DOMAIN}/api/sns/web/v1/search/notes"  # 搜索笔记
    SEARCH_USERS = f"{DOMAIN}/api/sns/web/v1/search/users"  # 搜索用户
    
    # 收藏相关接口 (需要登录)
    USER_COLLECT = f"{DOMAIN}/api/sns/web/v1/user_collect"  # 用户收藏
    
    # 首页推荐
    HOME_FEED = f"{DOMAIN}/api/sns/web/v1/homefeed"  # 首页推荐


class XiaohongshuHeaders:
    """小红书请求头模板"""
    
    DEFAULT = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.xiaohongshu.com",
        "pragma": "no-cache",
        "referer": "https://www.xiaohongshu.com/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
