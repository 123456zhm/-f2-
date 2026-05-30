#!/usr/bin/env python3
"""
测试抖音 Cookie 模式解析
"""
import sys
import os
import requests

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2'))

from f2.utils.conf_manager import ConfigManager
from f2.apps.douyin.handler import DouyinHandler
import asyncio

# 读取配置
config_path = os.path.join(os.path.dirname(__file__), 'f2', 'f2', 'conf', 'app.yaml')
cm = ConfigManager(config_path)

print("=" * 60)
print("测试抖音 Cookie 模式解析")
print("=" * 60)

# 抖音分享链接
share_url = "https://v.douyin.com/fhMP1liubHw/"

print(f"\n[1] 处理抖音分享链接")
print(f"    原始链接: {share_url}")

# 先获取重定向后的真实链接
try:
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    response = session.head(share_url, allow_redirects=False, timeout=10)
    
    if response.status_code in (301, 302, 303, 307, 308):
        real_url = response.headers.get('Location', '')
        print(f"    [OK] 重定向链接: {real_url}")
    else:
        real_url = share_url
        print(f"    [WARN] 未检测到重定向，使用原始链接")
        
except Exception as e:
    print(f"    [FAIL] 获取重定向失败: {e}")
    real_url = share_url

print(f"\n[2] 测试 Cookie 配置")
dy_cookie = cm.get("douyin.cookie", "")
print(f"    Cookie 长度: {len(dy_cookie)} 字符")

if not dy_cookie:
    print(f"    [FAIL] Cookie 为空！请在小程序中配置抖音 Cookie")
    sys.exit(1)

print(f"\n[3] 创建 Handler")
try:
    handler = DouyinHandler({
        "mode": "cookie",
        "cookie": dy_cookie,
        "tikhub_api_key": "",
        "tikhub_is_cn_user": True
    })
    print(f"    [OK] Handler 创建成功")
except Exception as e:
    print(f"    [FAIL] Handler 创建失败: {e}")
    sys.exit(1)

print(f"\n[4] 开始解析视频")
try:
    # 使用 asyncio 运行异步方法
    result = asyncio.run(asyncio.wait_for(
        handler.fetch_one_video(real_url),
        timeout=30.0
    ))
    
    if result:
        data = result.to_dict()
        
        print(f"    [OK] 解析成功！")
        print(f"\n    视频信息：")
        print(f"    - 标题: {data.get('title', data.get('desc', 'N/A'))}")
        print(f"    - 作者: {data.get('nickname', 'N/A')}")
        print(f"    - 点赞数: {data.get('liked_count', 0)}")
        print(f"    - 视频链接: {data.get('video_url', 'N/A')[:80]}...")
        
        if data.get('video_url'):
            print(f"\n    [SUCCESS] Cookie 模式正常工作！")
        else:
            print(f"\n    [FAIL] 无法获取视频链接，Cookie 可能无效")
    else:
        print(f"    [FAIL] 解析返回空结果")
        
except asyncio.TimeoutError:
    print(f"    [FAIL] 解析超时（30秒）")
    print(f"    可能原因：Cookie 无效或网络问题")
    
except Exception as e:
    print(f"    [FAIL] 解析失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
