"""
小红书平台请求/响应数据模型
Xiaohongshu Data Models using Pydantic
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Any


class BaseRequestModel(BaseModel):
    """小红书基础请求模型"""
    image_formats: str = "jpg,webp,avif"
    xsec_source: str = "pc_note"


class UserProfileRequest(BaseRequestModel):
    """用户信息请求"""
    user_id: str = Field(..., description="用户ID")


class UserPostedRequest(BaseRequestModel):
    """用户发布的笔记列表请求"""
    user_id: str = Field(..., description="用户ID")
    num: int = Field(default=30, description="每页数量")
    cursor: str = Field(default="", description="分页游标")
    xsec_token: str = Field(default="", description="安全令牌")


class NoteDetailRequest(BaseRequestModel):
    """笔记详情请求"""
    source_note_id: str = Field(..., description="笔记ID")
    xsec_token: str = Field(default="", description="安全令牌")
    xsec_source: str = "pc_feed"
    extra: dict = Field(default_factory=lambda: {"need_body_topic": "1"})


class SearchNotesRequest(BaseRequestModel):
    """搜索笔记请求"""
    keyword: str = Field(..., description="搜索关键词")
    page: int = Field(default=1, description="页码")
    page_size: int = Field(default=20, description="每页数量")
    search_type: str = Field(default="notes", description="搜索类型")


# ============ 响应模型 ============

class UserInfo(BaseModel):
    """用户信息"""
    user_id: str = ""
    nickname: str = ""
    avatar: str = ""
    desc: str = ""
    ip_location: str = ""
    follows: int = 0
    fans: int = 0
    liked: int = 0


class InteractInfo(BaseModel):
    """互动信息"""
    liked_count: int = 0
    collected_count: int = 0
    comment_count: int = 0
    share_count: int = 0


class ImageInfo(BaseModel):
    """图片信息"""
    url: str = ""
    width: int = 0
    height: int = 0


class NoteCard(BaseModel):
    """笔记卡片信息"""
    note_id: str = ""
    title: str = ""
    desc: str = ""
    content_type: str = ""  # note(图文) 或 video(视频)
    time: int = 0  # 发布时间戳
    last_update_time: int = 0
    user: UserInfo = UserInfo()
    interact_info: InteractInfo = InteractInfo()
    image_list: List[ImageInfo] = []
    video_url: str = ""
    ip_location: str = ""
    tags: List[str] = []
    
    model_config = {"protected_namespaces": ()}


class NoteDetail(BaseModel):
    """笔记详情"""
    note_id: str = ""
    xsec_token: str = ""
    note_url: str = ""
    note_card: NoteCard = NoteCard()


class UserPostedResponse(BaseModel):
    """用户笔记列表响应"""
    success: bool = False
    notes: List[dict] = []
    has_more: bool = False
    cursor: str = ""
    total: int = 0


class SearchResponse(BaseModel):
    """搜索响应"""
    success: bool = False
    items: List[dict] = []
    has_more: bool = False
    cursor: str = ""
