# path: f2/apps/xiaohongshu/dl.py

import asyncio
from typing import List, Dict, Any
from pathlib import Path

from f2.dl.base_downloader import BaseDownloader
from f2.log.logger import logger
from f2.utils.utils import create_user_folder, format_file_name


class XiaohongshuDownloader(BaseDownloader):
    """小红书下载器"""
    
    def __init__(self, kwargs: dict = None):
        """
        初始化下载器
        
        Args:
            kwargs: 配置参数
        """
        self.kwargs = kwargs or {}
        
        # 获取下载路径
        self.download_path = Path(kwargs.get("path", "Download"))
        self.download_path.mkdir(parents=True, exist_ok=True)
        
        # 命名模板
        self.naming = kwargs.get("naming", "{create}_{title}")
        
        # 是否下载封面、文案
        self.download_cover = kwargs.get("cover", True)
        self.download_desc = kwargs.get("desc", True)
        
        # 调用父类初始化
        super().__init__(self.kwargs)
    
    async def download_note(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        下载单个笔记
        
        Args:
            note_data: 笔记数据
            
        Returns:
            下载结果
        """
        note_id = note_data.get("note_id", "")
        title = note_data.get("title", "")
        desc = note_data.get("desc", "")
        user_id = note_data.get("user_id", "")
        nickname = note_data.get("nickname", "")
        create_time = note_data.get("publish_time", "")
        note_type = note_data.get("model_type", "note")  # note/video
        
        # 创建用户文件夹
        user_path = create_user_folder(self.download_path, nickname or user_id)
        
        # 格式化文件名
        file_name = format_file_name(
            self.naming,
            {
                "note_id": note_id,
                "title": title[:50] if title else "",  # 标题限制长度
                "desc": desc[:100] if desc else "",
                "nickname": nickname,
                "user_id": user_id,
                "create": create_time,
                "type": note_type,
            }
        )
        
        result = {
            "note_id": note_id,
            "success": True,
            "files": []
        }
        
        try:
            # 下载图片
            if note_type == "note":
                images = note_data.get("image_list", [])
                for i, img in enumerate(images):
                    url = img.get("url", "")
                    if url:
                        img_path = user_path / f"{file_name}_{i+1}.jpg"
                        await self.download_file(url, img_path)
                        result["files"].append(str(img_path))
                        logger.info(f"下载图片: {img_path}")
            
            # 下载视频
            elif note_type == "video":
                video_url = note_data.get("video_url", "")
                if video_url:
                    video_path = user_path / f"{file_name}.mp4"
                    await self.download_file(video_url, video_path)
                    result["files"].append(str(video_path))
                    logger.info(f"下载视频: {video_path}")
            
            # 保存文案
            if self.download_desc and desc:
                desc_path = user_path / f"{file_name}.txt"
                with open(desc_path, "w", encoding="utf-8") as f:
                    f.write(f"标题: {title}\n\n")
                    f.write(f"正文: {desc}\n\n")
                    f.write(f"作者: {nickname}\n")
                    f.write(f"发布时间: {create_time}\n")
                    f.write(f"链接: https://www.xiaohongshu.com/explore/{note_id}\n")
                result["files"].append(str(desc_path))
                logger.info(f"保存文案: {desc_path}")
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.error(f"下载笔记 {note_id} 失败: {e}")
        
        return result
    
    async def download_notes_batch(
        self, 
        notes: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        批量下载笔记
        
        Args:
            notes: 笔记列表
            
        Returns:
            下载结果列表
        """
        results = []
        
        # 使用并发控制
        max_tasks = self.kwargs.get("max_tasks", 10)
        semaphore = asyncio.Semaphore(max_tasks)
        
        async def download_with_semaphore(note):
            async with semaphore:
                return await self.download_note(note)
        
        # 并发下载
        tasks = [download_with_semaphore(note) for note in notes]
        results = await asyncio.gather(*tasks)
        
        return results
    
    async def download_file(self, url: str, path: Path) -> bool:
        """
        下载单个文件
        
        Args:
            url: 文件 URL
            path: 保存路径
            
        Returns:
            是否成功
        """
        try:
            # 检查文件是否已存在
            if path.exists():
                logger.info(f"文件已存在，跳过: {path}")
                return True
            
            # 使用父类的下载方法
            await self.save_file(url, path)
            return True
        except Exception as e:
            logger.error(f"下载文件失败 {url}: {e}")
            return False