#!/usr/bin/env python3
"""
测试 Cookie 模式的解析功能
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f2'))

from f2.utils.conf_manager import ConfigManager
from f2.apps.xiaohongshu.handler import XiaohongshuHandler
from f2.apps.douyin.handler import DouyinHandler

# 读取配置
config_path = os.path.join(os.path.dirname(__file__), 'f2', 'f2', 'conf', 'app.yaml')
cm = ConfigManager(config_path)

print("=" * 60)
print("测试 Cookie 模式解析")
print("=" * 60)

# 测试小红书
print("\n【小红书 Cookie 配置】")
xhs_cookie = cm.get("xiaohongshu.cookie", "")
print(f"Cookie 长度: {len(xhs_cookie)} 字符")
print(f"Cookie 前100字符: {xhs_cookie[:100]}...")
print(f"Cookie 后50字符: ...{xhs_cookie[-50:]}")

# 验证 Cookie 关键字段
print("\n【验证小红书 Cookie 关键字段】")
key_fields = ['a1', 'web_session', 'webId', 'webBuild', 'xsecappid']
for field in key_fields:
    if field in xhs_cookie:
        print(f"  [OK] {field}: 存在")
    else:
        print(f"  [FAIL] {field}: 缺失")

# 测试抖音
print("\n【抖音 Cookie 配置】")
dy_cookie = cm.get("douyin.cookie", "")
print(f"Cookie 长度: {len(dy_cookie)} 字符")
print(f"Cookie 前100字符: {dy_cookie[:100]}...")

print("\n【验证抖音 Cookie 关键字段】")
dy_key_fields = ['sessionid', 'sid_tt', 'uid_tt', 'sid_guard']
for field in dy_key_fields:
    if field in dy_cookie:
        print(f"  [OK] {field}: 存在")
    else:
        print(f"  [FAIL] {field}: 缺失")

# 测试解析功能
print("\n" + "=" * 60)
print("测试解析功能")
print("=" * 60)

# 测试小红书解析
print("\n【测试小红书解析】")
try:
    handler = XiaohongshuHandler({"cookie": xhs_cookie})
    print(f"  [OK] 小红书 Handler 创建成功")

    # 尝试解析一个示例链接（需要真实的笔记ID）
    test_url = "https://www.xiaohongshu.com/explore/123"
    print(f"  [WARN] 需要真实的小红书链接进行测试")
    print(f"  [WARN] 当前配置的 Cookie 可能无效（a1 字段看起来是随机字符串）")

except Exception as e:
    print(f"  [FAIL] 小红书 Handler 创建失败: {e}")

# 测试抖音解析
print("\n【测试抖音解析】")
try:
    handler = DouyinHandler({
        "mode": "cookie",
        "cookie": dy_cookie
    })
    print(f"  [OK] 抖音 Handler 创建成功")
    print(f"  [WARN] 需要真实的抖音链接进行测试")

except Exception as e:
    print(f"  [FAIL] 抖音 Handler 创建失败: {e}")

print("\n" + "=" * 60)
print("建议")
print("=" * 60)
print("1. 小红书 Cookie 的 'a1' 字段值看起来像是随机字符串")
print("2. 请从浏览器重新获取真实的小红书 Cookie")
print("3. 获取方法：")
print("   - 打开浏览器，登录小红书网页版")
print("   - 按 F12 打开开发者工具")
print("   - 在 Network 标签中找到任意请求")
print("   - 复制 Request Headers 中的 Cookie")
print("4. 抖音 Cookie 看起来正常，但需要真实链接测试")
