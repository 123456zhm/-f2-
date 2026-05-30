import aiohttp
import asyncio
import os
from typing import Optional, Dict, Any


class BaseDownloader:
    """基础下载器类"""
    
    def __init__(self, kwargs: dict = None):
        self.kwargs = kwargs or {}
        self.timeout = self.kwargs.get("timeout", 10)
        self.max_retries = self.kwargs.get("max_retries", 3)
        self.save_path = self.kwargs.get("path", "Download")
        self.max_connections = self.kwargs.get("max_connections", 5)
        self.semaphore = asyncio.Semaphore(self.max_connections)
        self.session = None
    
    async def __aenter__(self):
        """异步上下文管理器进入"""
        await self._create_session()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        """异步上下文管理器退出"""
        await self._close_session()
    
    async def _create_session(self):
        """创建 HTTP 会话"""
        connector = aiohttp.TCPConnector(limit_per_host=self.max_connections)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(connector=connector, timeout=timeout)
    
    async def _close_session(self):
        """关闭 HTTP 会话"""
        if self.session:
            await self.session.close()
    
    async def _download_file(self, url: str, save_path: str) -> bool:
        """下载单个文件"""
        try:
            async with self.semaphore:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        os.makedirs(os.path.dirname(save_path), exist_ok=True)
                        with open(save_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(1024):
                                f.write(chunk)
                        return True
                    return False
        except Exception as e:
            return False
    
    async def download(self, url: str, filename: str) -> bool:
        """下载文件到指定路径"""
        save_path = os.path.join(self.save_path, filename)
        return await self._download_file(url, save_path)
    
    async def download_batch(self, urls: list, filenames: list) -> list:
        """批量下载文件"""
        tasks = [
            self.download(url, filename)
            for url, filename in zip(urls, filenames)
        ]
        return await asyncio.gather(*tasks)