#!/usr/bin/env python3
"""
详细测试抖音 Cookie 模式 - 打印完整响应
"""
import sys
import os
import asyncio
import aiohttp
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2'))

from f2.utils.conf_manager import ConfigManager

# 读取配置
config_path = os.path.join(os.path.dirname(__file__), 'f2', 'f2', 'conf', 'app.yaml')
cm = ConfigManager(config_path)

print("=" * 60)
print("测试抖音 API 直接请求")
print("=" * 60)

# 抖音分享链接
share_url = "https://v.douyin.com/fhMP1liubHw/"

# 先获取重定向后的真实链接
print(f"\n[1] 获取重定向链接")
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})
response = session.head(share_url, allow_redirects=True, timeout=10)
real_url = response.url if hasattr(response, 'url') else share_url
print(f"    真实链接: {real_url}")

# 提取视频ID
import re
video_id_match = re.search(r'/video/(\d+)', real_url)
if not video_id_match:
    print(f"    [FAIL] 无法提取视频ID")
    sys.exit(1)

video_id = video_id_match.group(1)
print(f"    视频ID: {video_id}")

print(f"\n[2] 准备请求头")
cookie = cm.get("douyin.cookie", "")
print(f"    Cookie 长度: {len(cookie)}")

# 构建请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.douyin.com/',
    'Cookie': cookie,
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Origin': 'https://www.douyin.com',
}

print(f"\n[3] 发送 API 请求")
api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}"

# 添加常见参数
params = {
    'aid': '6383',
    'count': '1',
    'version_name': '5.1.2',
    'version_code': '50102',
    'device_platform': 'webapp',
    'os': 'windows',
    'SSMix': '1',
    'improvement_sincerely_thread': '1',
    'share_douyin': '1',
}

print(f"    API: {api_url}")
print(f"    参数: {params}")

try:
    response = requests.get(api_url, headers=headers, params=params, timeout=15)
    print(f"\n[4] 响应结果")
    print(f"    状态码: {response.status_code}")
    print(f"    响应头: {dict(response.headers)}")
    
    try:
        data = response.json()
        print(f"\n    响应 JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:2000])
    except:
        print(f"\n    响应文本:")
        print(response.text[:1000])
        
except Exception as e:
    print(f"    [FAIL] 请求失败: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
