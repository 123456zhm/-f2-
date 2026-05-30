"""
抖音平台请求/响应数据模型
Douyin Data Models using Pydantic
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any


class BaseRequestModel(BaseModel):
    pass


class UserInfoRequest(BaseRequestModel):
    user_id: str = Field(..., description="用户ID")
    sec_user_id: Optional[str] = Field("", description="加密用户ID")


class UserPostedRequest(BaseRequestModel):
    user_id: str = Field(..., description="用户ID")
    sec_user_id: Optional[str] = Field("", description="加密用户ID")
    max_cursor: int = Field(0, description="分页游标")
    count: int = Field(20, description="每页数量")


class VideoDetailRequest(BaseRequestModel):
    aweme_id: str = Field(..., description="视频ID")


class SearchRequest(BaseRequestModel):
    keyword: str = Field(..., description="搜索关键词")
    offset: int = Field(0, description="偏移量")
    count: int = Field(20, description="每页数量")
    search_source: int = Field(1, description="搜索来源")


class UserInfo(BaseModel):
    user_id: str = ""
    sec_user_id: str = ""
    nickname: str = ""
    avatar: str = ""
    signature: str = ""
    follower_count: int = 0
    following_count: int = 0
    total_favorited: int = 0
    aweme_count: int = 0


class VideoInfo(BaseModel):
    aweme_id: str = ""
    desc: str = ""
    duration: int = 0
    create_time: int = 0
    video_url: str = ""
    cover_url: str = ""
    play_url: str = ""
    width: int = 0
    height: int = 0


class VideoCard(BaseModel):
    aweme_id: str = ""
    desc: str = ""
    create_time: int = 0
    user: UserInfo = UserInfo()
    video: VideoInfo = VideoInfo()
    statistics: dict = {}
    share_url: str = ""


class VideoDetail(BaseModel):
    aweme_id: str = ""
    aweme_detail: VideoCard = VideoCard()


class UserPostedResponse(BaseModel):
    success: bool = False
    aweme_list: List[dict] = []
    has_more: bool = False
    max_cursor: int = 0


class SearchResponse(BaseModel):
    success: bool = False
    data: List[dict] = []
    has_more: bool = False
    cursor: int = 0