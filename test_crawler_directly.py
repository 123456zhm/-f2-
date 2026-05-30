#!/usr/bin/env python3
"""
直接测试 DouyinCrawler，打印完整响应
"""
import sys
import os
import asyncio
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2'))

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from f2.utils.conf_manager import ConfigManager
from f2.apps.douyin.crawler import DouyinCrawler

async def test():
    # 读取配置
    config_path = os.path.join(os.path.dirname(__file__), 'f2', 'f2', 'conf', 'app.yaml')
    cm = ConfigManager(config_path)
    
    cookie = cm.get("douyin.cookie", "")
    print(f"[test] Cookie 长度: {len(cookie)}")
    print(f"[test] Cookie 前200字符: {cookie[:200]}")
    
    # 创建 crawler
    kwargs = {
        "cookie": cookie,
        "proxies": {"http://": None, "https://": None}
    }
    
    print(f"\n[test] 创建 DouyinCrawler...")
    async with DouyinCrawler(kwargs) as crawler:
        print(f"[test] Crawler 创建成功")
        print(f"[test] Headers: {crawler.headers}")
        
        # 测试视频ID
        video_id = "7636490241968311592"
        print(f"\n[test] 获取视频详情, ID: {video_id}")
        
        from f2.apps.douyin.model import VideoDetailRequest
        params = VideoDetailRequest(aweme_id=video_id)
        
        try:
            response = await crawler.fetch_video_detail(params)
            print(f"\n[test] 响应结果:")
            import json
            print(json.dumps(response, indent=2, ensure_ascii=False, default=str)[:3000])
            
            # 检查 video 字段
            aweme_detail = response.get('aweme_detail', {})
            print(f"\n[test] aweme_detail 字段: {aweme_detail.keys()}")
            
            video = aweme_detail.get('video', {})
            print(f"[test] video 字段: {video.keys()}")
            
            play_addr = video.get('play_addr', {})
            print(f"[test] play_addr 字段: {play_addr.keys()}")
            
            url_list = play_addr.get('url_list', [])
            print(f"[test] url_list: {url_list}")
            
        except Exception as e:
            print(f"\n[test] 请求失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
