import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'f2'))

from f2.apps.douyin.handler import DouyinHandler
from f2.apps.douyin.tikhub_api import TikHubDouyinAPI
from f2.utils.conf_manager import ConfigManager

async def test_douyin_parse():
    config_path = os.path.join(os.path.dirname(__file__), 'f2', 'f2', 'conf', 'app.yaml')
    cm = ConfigManager(config_path)
    
    api_key = cm.get("douyin.tikhub_api_key", "")
    mode = cm.get("douyin.api_mode", "cookie")
    is_cn_user = cm.get("douyin.tikhub_is_cn_user", "yes") == "yes"
    
    print(f"Current mode: {mode}")
    print(f"API Key: {api_key[:20]}..." if api_key else "No API Key configured")
    print(f"CN User: {is_cn_user}")
    
    if mode == "tikhub" and api_key:
        tikhub_api = TikHubDouyinAPI(api_key, is_cn_user)
        url = "https://v.douyin.com/JSW_jXt13Cc/"
        
        print(f"\nTesting URL: {url}")
        print(f"API Base URL: {tikhub_api.base_url}")
        
        response = tikhub_api.fetch_video_detail_by_url(url)
        print(f"\nRaw API Response:")
        print(str(response)[:2000] + "..." if len(str(response)) > 2000 else str(response))
        
        if response.get('success') == False or 'error' in response:
            print("\nAPI Request failed!")
            print(f"Error: {response.get('error', 'Unknown error')}")
            return
    
    handler = DouyinHandler({
        "mode": mode,
        "tikhub_api_key": api_key,
        "tikhub_is_cn_user": is_cn_user
    })
    
    url = "https://v.douyin.com/JSW_jXt13Cc/"
    
    try:
        result = await handler.fetch_one_video(url)
        video_dict = result.to_dict()
        
        print("\nParse result:")
        print(f"Title: {video_dict.get('title', 'Unknown')}")
        print(f"Author: {video_dict.get('author', 'Unknown')}")
        print(f"Video URL: {video_dict.get('video_url', 'Unknown')}")
        print(f"Cover URL: {video_dict.get('cover_url', 'Unknown')}")
        
        if not video_dict.get('video_url'):
            print("\nWARNING: Video URL is empty!")
            print(f"Full video dict: {video_dict}")
            
    except Exception as e:
        print("ERROR: Parse failed:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_douyin_parse())