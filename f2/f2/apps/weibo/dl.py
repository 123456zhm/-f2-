# path: f2/apps/weibo/dl.py

import asyncio
from typing import List, Dict, Any
from pathlib import Path

from f2.dl.base_downloader import BaseDownloader
from f2.log.logger import logger
from f2.utils.utils import create_user_folder, format_file_name


class WeiboDownloader(BaseDownloader):
    def __init__(self, kwargs: dict = None):
        self.kwargs = kwargs or {}
        self.download_path = Path(kwargs.get("path", "Download"))
        self.download_path.mkdir(parents=True, exist_ok=True)
        self.naming = kwargs.get("naming", "{create}_{title}")
        self.download_cover = kwargs.get("cover", True)
        self.download_desc = kwargs.get("desc", True)
        super().__init__(self.kwargs)

    async def download_status(self, status_data: Dict[str, Any]) -> Dict[str, Any]:
        status_id = status_data.get("status_id", "")
        title = status_data.get("title", "")
        desc = status_data.get("desc", "")
        user_id = status_data.get("user_id", "")
        nickname = status_data.get("nickname", "")
        create_time = status_data.get("publish_time", "")
        image_list = status_data.get("image_list", [])
        video_url = status_data.get("video_url", "")

        user_path = create_user_folder(self.download_path, nickname or user_id)

        file_name = format_file_name(
            self.naming,
            {
                "status_id": status_id,
                "title": title[:50] if title else "",
                "desc": desc[:100] if desc else "",
                "nickname": nickname,
                "user_id": user_id,
                "create": create_time.replace(' ', '_'),
                "type": "weibo",
            }
        )

        result = {
            "status_id": status_id,
            "success": True,
            "files": []
        }

        try:
            if image_list:
                for i, img in enumerate(image_list):
                    url = img.get("url", "")
                    if url:
                        img_path = user_path / f"{file_name}_{i+1}.jpg"
                        await self.download_file(url, img_path)
                        result["files"].append(str(img_path))
                        logger.info(f"下载图片: {img_path}")

            if video_url:
                video_path = user_path / f"{file_name}.mp4"
                await self.download_file(video_url, video_path)
                result["files"].append(str(video_path))
                logger.info(f"下载视频: {video_path}")

            if self.download_desc and desc:
                desc_path = user_path / f"{file_name}.txt"
                with open(desc_path, "w", encoding="utf-8") as f:
                    f.write(f"标题: {title}\n\n")
                    f.write(f"正文: {desc}\n\n")
                    f.write(f"作者: {nickname}\n")
                    f.write(f"发布时间: {create_time}\n")
                    f.write(f"链接: https://weibo.com/{user_id}/{status_id}\n")
                result["files"].append(str(desc_path))
                logger.info(f"保存文案: {desc_path}")

        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            logger.error(f"下载微博 {status_id} 失败: {e}")

        return result

    async def download_statuses_batch(
        self,
        statuses: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        results = []
        max_tasks = self.kwargs.get("max_tasks", 10)
        semaphore = asyncio.Semaphore(max_tasks)

        async def download_with_semaphore(status):
            async with semaphore:
                return await self.download_status(status)

        tasks = [download_with_semaphore(status) for status in statuses]
        results = await asyncio.gather(*tasks)

        return results

    async def download_file(self, url: str, path: Path) -> bool:
        try:
            if path.exists():
                logger.info(f"文件已存在，跳过: {path}")
                return True

            await self.save_file(url, path)
            return True
        except Exception as e:
            logger.error(f"下载文件失败 {url}: {e}")
            return False