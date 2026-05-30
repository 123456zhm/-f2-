from fastapi import FastAPI, HTTPException, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from f2.apps.xiaohongshu.handler import XiaohongshuHandler
from f2.apps.douyin.handler import DouyinHandler
from f2.apps.weibo.handler import WeiboHandler

app = FastAPI(title="免费去水印工具 API", description="支持小红薯、抖海、围脖的视频解析服务", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ParseRequest(BaseModel):
    url: str
    platform: Optional[str] = None

class ParseResult(BaseModel):
    success: bool
    type: Optional[str] = None
    cover: Optional[str] = None
    title: Optional[str] = None
    desc: Optional[str] = None
    author: Optional[str] = None
    time: Optional[str] = None
    likes: Optional[str] = None
    comments: Optional[str] = None
    shares: Optional[str] = None
    images: Optional[List[str]] = None
    videoUrl: Optional[str] = None
    downloadUrl: Optional[str] = None
    error: Optional[str] = None

def detect_platform(url: str) -> Optional[str]:
    if 'xiaohongshu' in url or 'xhslink' in url or 'xiaohongshu.com' in url:
        return 'xiaohongshu'
    elif 'douyin' in url or 'dytt' in url or 'amemv.com' in url:
        return 'douyin'
    elif 'weibo' in url or 'weibo.com' in url:
        return 'weibo'
    return None

def parse_xiaohongshu(url: str) -> Dict[str, Any]:
    try:
        import os
        from f2.utils.conf_manager import ConfigManager

        config_path = os.path.join(os.path.dirname(__file__), 'f2', 'conf', 'app.yaml')
        cm = ConfigManager(config_path)

        api_mode = cm.get("xiaohongshu.api_mode", "cookie")
        api_key = cm.get("xiaohongshu.tikhub_api_key", "")
        is_cn_user = cm.get("xiaohongshu.tikhub_is_cn_user", "yes") == "yes"
        cookie = cm.get("xiaohongshu.cookie", "")

        # 确保短链接使用 https
        if url.startswith('http://xhslink.com'):
            url = 'https://' + url[7:]

        if api_mode == "tikhub" and api_key:
            handler = XiaohongshuHandler({
                "mode": "tikhub",
                "tikhub_api_key": api_key,
                "tikhub_is_cn_user": is_cn_user
            })
            result = handler.fetch_one_note(url)
        else:
            if not cookie:
                return {"success": False, "error": "未配置小红书Cookie，请先在设置页面配置Cookie"}
            handler = XiaohongshuHandler({"cookie": cookie})
            result = handler.fetch_one_note(url)

        if result and hasattr(result, 'to_dict'):
            data = result.to_dict()
            # 检查是否成功获取到数据（title为空说明请求失败）
            if not data.get('title') and not data.get('video_url') and not data.get('image_list'):
                return {"success": False, "error": "解析失败，请检查Cookie是否有效（Cookie可能已过期，请重新获取）"}
            return {
                "success": True,
                "type": "video" if data.get('video_url') else "note",
                "cover": (data.get('image_list') or [{}])[0].get('url', '') if data.get('image_list') else data.get('user_avatar', ''),
                "title": data.get('title'),
                "desc": data.get('desc'),
                "author": data.get('user_nickname'),
                "time": data.get('publish_time'),
                "likes": str(data.get('liked_count', 0)),
                "comments": str(data.get('comment_count', 0)),
                "shares": str(data.get('share_count', 0)),
                "images": [img.get('url') for img in (data.get('image_list') or [])],
                "videoUrl": data.get('video_url'),
                "downloadUrl": data.get('video_url') or ((data.get('image_list') or [{}])[0].get('url', '') if data.get('image_list') else "")
            }
        return {"success": False, "error": "解析失败"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def parse_douyin(url: str) -> Dict[str, Any]:
    try:
        import asyncio
        import logging
        from f2.utils.conf_manager import ConfigManager

        # 添加日志
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        config_path = os.path.join(os.path.dirname(__file__), 'f2', 'conf', 'app.yaml')
        cm = ConfigManager(config_path)

        api_key = cm.get("douyin.tikhub_api_key", "")
        mode = cm.get("douyin.api_mode", "cookie")
        is_cn_user = cm.get("douyin.tikhub_is_cn_user", "yes") == "yes"
        cookie = cm.get("douyin.cookie", "")

        logger.info(f"[parse_douyin] mode={mode}, cookie_len={len(cookie)}, url={url[:50]}")

        handler = DouyinHandler({
            "mode": mode,
            "cookie": cookie,
            "tikhub_api_key": api_key,
            "tikhub_is_cn_user": is_cn_user
        })

        try:
            result = asyncio.run(asyncio.wait_for(
                handler.fetch_one_video(url),
                timeout=25.0
            ))
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": "⏰ API解析超时\n\n可能原因：\n1. 网络连接不稳定\n2. TikHub服务器响应慢\n3. 请稍后重试"
            }

        if result:
            data = result.to_dict()

            video_url = data.get('video_url', '')
            cover_url = data.get('cover_url', '')

            if not video_url:
                return {
                    "success": False,
                    "error": "无法获取视频下载地址\n\n可能原因：\n1. 视频已被删除或设为私密\n2. 视频链接已过期\n3. 网络请求失败，请重试"
                }

            if cover_url and (not cover_url.startswith('http') or len(cover_url) < 20):
                cover_url = ''

            return {
                "success": True,
                "type": "video",
                "cover": cover_url if cover_url and cover_url.startswith('http') else None,
                "title": data.get('title') or data.get('desc', '抖音视频')[:50],
                "desc": data.get('desc'),
                "author": data.get('nickname', '未知用户'),
                "time": data.get('publish_time'),
                "likes": str(data.get('liked_count', 0)),
                "comments": str(data.get('comment_count', 0)),
                "shares": str(data.get('share_count', 0)),
                "images": [],
                "videoUrl": video_url,
                "downloadUrl": video_url
            }
        return {"success": False, "error": "解析失败：未获取到视频数据"}
    except asyncio.TimeoutError:
        return {"success": False, "error": "解析超时\n\n请检查网络后重试"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": f"解析失败: {str(e)}"}

def parse_weibo(url: str) -> Dict[str, Any]:
    try:
        import os
        from f2.utils.conf_manager import ConfigManager

        config_path = os.path.join(os.path.dirname(__file__), 'f2', 'conf', 'app.yaml')
        cm = ConfigManager(config_path)

        cookie = cm.get("weibo.cookie", "")

        handler = WeiboHandler({"cookie": cookie})
        result = handler.fetch_one_status(url)

        if result and hasattr(result, '__dict__'):
            data = result.__dict__
            return {
                "success": True,
                "type": "video" if data.get('video') else "note",
                "cover": data.get('cover'),
                "title": data.get('text')[:50] if data.get('text') else "微博内容",
                "desc": data.get('text'),
                "author": data.get('nickname'),
                "time": data.get('created_at'),
                "likes": str(data.get('likes_count', 0)),
                "comments": str(data.get('comments_count', 0)),
                "shares": str(data.get('reposts_count', 0)),
                "images": data.get('images', []),
                "videoUrl": data.get('video'),
                "downloadUrl": data.get('video') or (data.get('images')[0] if data.get('images') else "")
            }
        return {"success": False, "error": "解析失败"}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/parse", response_model=ParseResult)
def parse_link(request: ParseRequest):
    url = request.url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="请提供链接")

    platform = request.platform or detect_platform(url)

    if not platform:
        raise HTTPException(status_code=400, detail="无法识别链接平台")

    try:
        if platform == 'xiaohongshu':
            result = parse_xiaohongshu(url)
        elif platform == 'douyin':
            result = parse_douyin(url)
        elif platform == 'weibo':
            result = parse_weibo(url)
        else:
            raise HTTPException(status_code=400, detail="不支持的平台")

        if not result['success']:
            raise HTTPException(status_code=500, detail=result.get('error', '解析失败'))

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.get("/api/stream")
async def stream_video(url: str, range: Optional[str] = Header(None)):
    if not url:
        raise HTTPException(status_code=400, detail="请提供视频URL")

    try:
        # 根据视频来源设置不同的 Referer
        if 'douyin' in url or 'douyinvod' in url:
            referer = 'https://www.douyin.com/'
        elif 'xiaohongshu' in url or 'xhscdn' in url:
            referer = 'https://www.xiaohongshu.com/'
        else:
            referer = ''

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        if referer:
            headers['Referer'] = referer
        
        if range:
            headers['Range'] = range

        response = requests.get(url, headers=headers, stream=True, timeout=(10, 60))

        if response.status_code not in (200, 206):
            raise HTTPException(status_code=response.status_code, detail="无法获取视频")

        content_length = response.headers.get('content-length')
        content_type = response.headers.get('content-type', 'video/mp4')
        accept_ranges = response.headers.get('accept-ranges', 'bytes')

        stream_headers = {
            'Content-Type': content_type,
            'Accept-Ranges': accept_ranges,
        }

        if 'Content-Range' in response.headers:
            stream_headers['Content-Range'] = response.headers['Content-Range']
        elif content_length:
            stream_headers['Content-Length'] = content_length

        return StreamingResponse(
            response.iter_content(chunk_size=1024 * 1024),
            media_type=content_type,
            headers=stream_headers,
            status_code=response.status_code
        )
    except requests.Timeout:
        raise HTTPException(status_code=504, detail="视频下载超时")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"下载失败: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "服务正常运行"}

@app.get("/api/platforms")
def get_platforms():
    return {
        "platforms": [
            {"name": "小红薯", "key": "xiaohongshu", "color": "#ff2442", "icon": "📕"},
            {"name": "抖海", "key": "douyin", "color": "#161823", "icon": "🎵"},
            {"name": "围脖", "key": "weibo", "color": "#ff8200", "icon": "📱"}
        ]
    }

@app.get("/api/config")
def get_config():
    from f2.utils.conf_manager import ConfigManager
    config_path = os.path.join(os.path.dirname(__file__), 'f2', 'conf', 'app.yaml')
    cm = ConfigManager(config_path)
    
    return {
        "success": True,
        "config": {
            "douyin": {
                "api_mode": cm.get("douyin.api_mode", "cookie"),
                "has_cookie": bool(cm.get("douyin.cookie", "")),
                "has_api_key": bool(cm.get("douyin.tikhub_api_key", ""))
            },
            "xiaohongshu": {
                "api_mode": cm.get("xiaohongshu.api_mode", "cookie"),
                "has_cookie": bool(cm.get("xiaohongshu.cookie", "")),
                "has_api_key": bool(cm.get("xiaohongshu.tikhub_api_key", ""))
            },
            "weibo": {
                "has_cookie": bool(cm.get("weibo.cookie", ""))
            }
        }
    }

class ConfigUpdateRequest(BaseModel):
    platform: str
    api_mode: Optional[str] = None
    cookie: Optional[str] = None
    tikhub_api_key: Optional[str] = None

@app.post("/api/cookie/simplify")
def simplify_cookie(request_data: dict):
    """简化 Cookie，只保留核心字段"""
    from f2.utils.cookie_simplifier import cookie_simplifier

    try:
        platform = request_data.get('platform', '')
        cookie = request_data.get('cookie', '')

        if not platform or not cookie:
            return {"success": False, "error": "缺少参数"}

        simplified = cookie_simplifier.simplify_cookie(cookie, platform)
        validation = cookie_simplifier.validate_cookie(simplified, platform)

        return {
            "success": True,
            "original_length": len(cookie),
            "simplified_length": len(simplified),
            "simplified_cookie": simplified,
            "validation": validation
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/cookie/validate")
def validate_cookie(request_data: dict):
    """验证 Cookie 是否有效"""
    from f2.utils.cookie_simplifier import cookie_simplifier

    try:
        platform = request_data.get('platform', '')
        cookie = request_data.get('cookie', '')

        if not platform or not cookie:
            return {"success": False, "error": "缺少参数"}

        validation = cookie_simplifier.validate_cookie(cookie, platform)
        return {"success": True, "validation": validation}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/cookie/detect-platform")
def detect_cookie_platform(request_data: dict):
    """检测 Cookie 所属平台"""
    from f2.utils.cookie_simplifier import cookie_simplifier

    try:
        cookie = request_data.get('cookie', '')

        if not cookie:
            return {"success": False, "error": "缺少参数"}

        platform = cookie_simplifier.detect_platform(cookie)
        return {"success": True, "platform": platform}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/api/config")
def update_config(request: ConfigUpdateRequest):
    import yaml
    from f2.utils.conf_manager import ConfigManager
    from f2.utils.cookie_simplifier import cookie_simplifier

    config_path = os.path.join(os.path.dirname(__file__), 'f2', 'conf', 'app.yaml')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        platform = request.platform
        if platform not in ['douyin', 'xiaohongshu', 'weibo']:
            raise HTTPException(status_code=400, detail="不支持的平台")

        if platform in config:
            if request.api_mode:
                config[platform]['api_mode'] = request.api_mode
            if request.cookie:
                original_cookie = request.cookie
                simplified_cookie = cookie_simplifier.simplify_cookie(original_cookie, platform)
                config[platform]['cookie'] = simplified_cookie
            if request.tikhub_api_key:
                config[platform]['tikhub_api_key'] = request.tikhub_api_key

        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        return {"success": True, "message": "配置已更新", "cookie_simplified": bool(request.cookie)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新配置失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
