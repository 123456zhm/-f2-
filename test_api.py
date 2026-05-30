import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'f2'))

async def test_api():
    from f2.apps.douyin.handler import DouyinHandler
    from f2.utils.conf_manager import ConfigManager
    
    config_path = os.path.join(os.path.dirname(__file__), 'f2', 'f2', 'conf', 'app.yaml')
    cm = ConfigManager(config_path)
    
    api_key = cm.get("douyin.tikhub_api_key", "")
    mode = cm.get("douyin.api_mode", "cookie")
    is_cn_user = cm.get("douyin.tikhub_is_cn_user", "yes") == "yes"
    
    print(f"Mode: {mode}")
    print(f"API Key: {api_key[:20]}..." if api_key else "No API Key")
    print(f"CN User: {is_cn_user}")
    
    handler = DouyinHandler({
        "mode": mode,
        "tikhub_api_key": api_key,
        "tikhub_is_cn_user": is_cn_user
    })
    
    url = "https://v.douyin.com/JSW_jXt13Cc/"
    
    try:
        result = await handler.fetch_one_video(url)
        data = result.to_dict()
        print("\nParse Result:")
        print(f"Title: {data.get('title', 'N/A')}")
        print(f"Author: {data.get('nickname', 'N/A')}")
        print(f"Video URL: {data.get('video_url', 'N/A')[:100]}..." if data.get('video_url') else "N/A")
        print(f"Cover URL: {data.get('cover_url', 'N/A')[:100]}..." if data.get('cover_url') else "N/A")
        return data.get('video_url') is not None
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_api())
    sys.exit(0 if success else 1)