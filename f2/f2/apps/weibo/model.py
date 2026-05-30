"""
微博平台请求/响应数据模型
Weibo Data Models using Pydantic
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any


class BaseRequestModel(BaseModel):
    pass


class UserInfoRequest(BaseRequestModel):
    uid: str = Field(..., description="用户ID")


class UserTimelineRequest(BaseRequestModel):
    uid: str = Field(..., description="用户ID")
    page: int = Field(1, description="页码")
    count: int = Field(20, description="每页数量")


class StatusDetailRequest(BaseRequestModel):
    id: str = Field(..., description="微博ID")


class SearchRequest(BaseRequestModel):
    keyword: str = Field(..., description="搜索关键词")
    page: int = Field(1, description="页码")
    count: int = Field(20, description="每页数量")


class UserInfo(BaseModel):
    id: str = ""
    screen_name: str = ""
    profile_image_url: str = ""
    description: str = ""
    followers_count: int = 0
    follow_count: int = 0
    statuses_count: int = 0
    favourites_count: int = 0


class PictureInfo(BaseModel):
    url: str = ""
    width: int = 0
    height: int = 0


class StatusCard(BaseModel):
    id: str = ""
    idstr: str = ""
    text: str = ""
    created_at: str = ""
    user: UserInfo = UserInfo()
    reposts_count: int = 0
    comments_count: int = 0
    attitudes_count: int = 0
    pic_urls: List[PictureInfo] = []
    retweeted_status: dict = {}
    video_url: str = ""


class UserTimelineResponse(BaseModel):
    success: bool = False
    statuses: List[dict] = []
    has_more: bool = False
    total: int = 0


class SearchResponse(BaseModel):
    success: bool = False
    cards: List[dict] = []
    has_more: bool = False
    total_number: int = 0