#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikHub API 测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'f2'))

from f2.utils.conf_manager import ConfigManager
from f2.apps.xiaohongshu.handler import XiaohongshuHandler
from f2.apps.douyin.handler import DouyinHandler
from f2.log.logger import logger


def get_config_manager():
    """获取配置管理器"""
    # 尝试多个路径
    config_paths = [
        os.path.join(os.path.dirname(__file__), 'f2', 'f2', 'conf', 'app.yaml'),
        'f2/f2/conf/app.yaml',
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            logger.info(f"✅ 找到配置文件: {path}")
            return ConfigManager(path)
    
    logger.error(f"❌ 找不到配置文件！尝试路径: {config_paths}")
    return None


def test_xiaohongshu_tikhub():
    """测试小红书 TikHub 模式"""
    logger.info("=" * 60)
    logger.info("测试小红书 TikHub API")
    logger.info("=" * 60)
    
    try:
        # 读取配置
        cm = get_config_manager()
        if not cm:
            return False
        
        api_key = cm.get("xiaohongshu.tikhub_api_key", "")
        
        if not api_key:
            logger.error("❌ 未配置小红书 TikHub API Key，请检查 f2/conf/app.yaml")
            return False
        
        logger.info(f"✅ API Key 已加载: {api_key[:10]}...")
        
        # 初始化处理器
        handler = XiaohongshuHandler({
            "mode": "tikhub",
            "tikhub_api_key": api_key,
            "tikhub_is_cn_user": cm.get("xiaohongshu.tikhub_is_cn_user", True)
        })
        
        # 测试用的小红书笔记链接
        test_url = "https://www.xiaohongshu.com/explore/6475c4a80000000027038d9a"
        
        logger.info(f"🔗 测试链接: {test_url}")
        
        # 获取笔记详情
        result = handler.fetch_one_note(test_url)
        
        if hasattr(result, 'to_dict'):
            data = result.to_dict()
            logger.info(f"✅ 成功获取笔记: {data.get('title', '无标题')}")
            logger.info(f"   笔记 ID: {data.get('note_id', '')}")
            logger.info(f"   作者: {data.get('user_nickname', '')}")
            logger.info(f"   笔记类型: {data.get('model_type', '')}")
            
            if data.get('model_type') == 'video':
                logger.info(f"   视频链接: {data.get('video_url', '')[:50]}...")
            
            return True
        else:
            logger.error("❌ 返回结果异常")
            return False
            
    except Exception as e:
        logger.error(f"❌ 小红书测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_douyin_tikhub():
    """测试抖音 TikHub 模式"""
    logger.info("\n" + "=" * 60)
    logger.info("测试抖音 TikHub API")
    logger.info("=" * 60)
    
    try:
        # 读取配置
        cm = get_config_manager()
        if not cm:
            return False
        
        api_key = cm.get("douyin.tikhub_api_key", "")
        
        if not api_key:
            logger.error("❌ 未配置抖音 TikHub API Key，请检查 f2/conf/app.yaml")
            return False
        
        logger.info(f"✅ API Key 已加载: {api_key[:10]}...")
        
        # 初始化处理器
        handler = DouyinHandler({
            "mode": "tikhub",
            "tikhub_api_key": api_key,
            "tikhub_is_cn_user": cm.get("douyin.tikhub_is_cn_user", True)
        })
        
        # 测试用的抖音视频链接
        test_url = "https://v.douyin.com/6Z2dWJ/"
        
        logger.info(f"🔗 测试链接: {test_url}")
        
        # 获取视频详情（注意这是 async 函数，需要用 asyncio 运行）
        import asyncio
        result = asyncio.run(handler.fetch_one_video(test_url))
        
        if hasattr(result, 'to_dict'):
            data = result.to_dict()
            logger.info(f"✅ 成功获取视频: {data.get('desc', '无描述')[:50]}...")
            logger.info(f"   视频 ID: {data.get('aweme_id', '')}")
            logger.info(f"   作者: {data.get('nickname', '')}")
            
            return True
        else:
            logger.error("❌ 返回结果异常")
            return False
            
    except Exception as e:
        logger.error(f"❌ 抖音测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    logger.info("\n🚀 开始测试 TikHub API 配置")
    logger.info("=" * 60)
    
    success_count = 0
    total_tests = 0
    
    # 测试小红书
    total_tests += 1
    if test_xiaohongshu_tikhub():
        success_count += 1
    
    # 测试抖音
    total_tests += 1
    if test_douyin_tikhub():
        success_count += 1
    
    # 总结
    logger.info("\n" + "=" * 60)
    logger.info(f"测试完成: {success_count}/{total_tests} 成功")
    logger.info("=" * 60)
    
    if success_count == total_tests:
        logger.info("🎉 所有测试通过！TikHub API 配置正确！")
        return 0
    else:
        logger.warning("⚠️ 部分测试失败，请检查配置")
        return 1


if __name__ == "__main__":
    exit(main())
