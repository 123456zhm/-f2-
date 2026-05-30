import aiohttp
import asyncio
from typing import Optional, Dict, Any


class BaseCrawler:
    """基础爬虫类"""
    
    def __init__(self, kwargs: dict = None, proxies: dict = None, crawler_headers: dict = None):
        self.kwargs = kwargs or {}
        self.proxies = proxies or {"http://": None, "https://": None}
        self.headers = crawler_headers or {}
        self.timeout = self.kwargs.get("timeout", 10)
        self.max_retries = self.kwargs.get("max_retries", 3)
        self.session = None
    
    async def __aenter__(self):
        await self._create_session()
        return self
    
    async def __aexit__(self, exc_type, exc, tb):
        await self._close_session()
    
    async def _create_session(self):
        connector = aiohttp.TCPConnector(limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        
        session_kwargs = {
            "connector": connector,
            "timeout": timeout,
            "headers": self.headers
        }
        
        if self.proxies and self.proxies.get("http://"):
            session_kwargs["connector"] = aiohttp.TCPConnector(
                limit_per_host=5,
                proxy=self.proxies.get("http://")
            )
        
        self.session = aiohttp.ClientSession(**session_kwargs)
    
    async def _close_session(self):
        if self.session:
            await self.session.close()
    
    async def _retry_request(self, method: str, url: str, **kwargs) -> aiohttp.ClientResponse:
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                # 不使用 async with，避免退出 context 时释放 connection
                # 导致调用方无法读取 response body
                response = await self.session.request(method, url, **kwargs)
                return response
            except Exception as e:
                retry_count += 1
                if retry_count < self.max_retries:
                    await asyncio.sleep(1 * retry_count)
                else:
                    raise e
    
    async def get_fetch_data(self, url: str, headers: dict = None) -> aiohttp.ClientResponse:
        request_headers = {**self.headers, **(headers or {})}
        return await self._retry_request("GET", url, headers=request_headers)
    
    async def post_fetch_data(self, url: str, data: str = None, headers: dict = None) -> aiohttp.ClientResponse:
        request_headers = {**self.headers, **(headers or {})}
        return await self._retry_request("POST", url, data=data, headers=request_headers)
    
    async def download_file(self, url: str, save_path: str) -> bool:
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    with open(save_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(1024):
                            f.write(chunk)
                    return True
                return False
        except Exception as e:
            return False
