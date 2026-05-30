"""
小红书数据过滤器
Xiaohongshu Data Filter
"""

import re
from typing import List, Optional
from datetime import datetime


class UserProfileFilter:
    """用户信息过滤器"""
    
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('data', {})
    
    @property
    def user_id(self) -> str:
        return self._data.get('user_id', '')
    
    @property
    def nickname(self) -> str:
        return self._data.get('nickname', '')
    
    @property
    def avatar(self) -> str:
        return self._data.get('image', '')
    
    @property
    def desc(self) -> str:
        return self._data.get('desc', '')
    
    @property
    def ip_location(self) -> str:
        return self._data.get('ip_location', '')
    
    @property
    def follows(self) -> int:
        return self._data.get('follows', 0)
    
    @property
    def fans(self) -> int:
        return self._data.get('fans', 0)
    
    @property
    def liked(self) -> int:
        return self._data.get('liked', 0)
    
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'avatar': self.avatar,
            'desc': self.desc,
            'ip_location': self.ip_location,
            'follows': self.follows,
            'fans': self.fans,
            'liked': self.liked,
        }


class NoteCardFilter:
    """笔记卡片过滤器
    
    同时兼容两种数据格式:
    1. API 返回格式 (snake_case: note_card, model_type, interact_info, image_list 等)
    2. 网页端格式 (camelCase: noteId, type, interactInfo, imageList 等)
    """
    
    def __init__(self, data: dict, xsec_token: str = ""):
        self.raw = data
        self._xsec_token = xsec_token
        
        # 获取 note_card 数据
        if 'note_card' in data:
            self._card = data['note_card']
        else:
            self._card = data
    
    @property
    def note_id(self) -> str:
        return self.raw.get('id', '') or self.raw.get('note_id', '') or self.raw.get('noteId', '')
    
    @property
    def xsec_token(self) -> str:
        return self._xsec_token or self.raw.get('xsec_token', '') or self.raw.get('xsecToken', '')
    
    @property
    def note_url(self) -> str:
        return f"https://www.xiaohongshu.com/explore/{self.note_id}?xsec_token={self.xsec_token}&xsec_source=pc_feed"
    
    @property
    def model_type(self) -> str:
        """note=图文, video=视频"""
        # API: model_type, 网页端: type
        mtype = self.raw.get('model_type', '') or self.raw.get('type', '')
        # 网页端 type=normal 对应图文, type=video 对应视频
        if mtype == 'normal':
            return 'note'
        return mtype or 'note'
    
    @property
    def title(self) -> str:
        return self._card.get('title', '')
    
    @property
    def desc(self) -> str:
        return self._card.get('desc', '')
    
    @property
    def tags(self) -> List[str]:
        """提取标签"""
        desc = self.desc
        # 匹配 #标签[话题] 格式
        tags = re.findall(r'#([^#\[\]]+)(?=\[话题\])', desc)
        # 也从 tagList 提取（网页端格式）
        tag_list = self._card.get('tagList', [])
        if tag_list and isinstance(tag_list, list):
            for tag in tag_list:
                tag_name = tag.get('name', '') or tag.get('#', '')
                if tag_name and tag_name not in tags:
                    tags.append(tag_name)
        return tags
    
    @property
    def publish_time(self) -> str:
        """发布时间"""
        timestamp = self._card.get('time', 0)
        if timestamp:
            return self._convert_timestamp(timestamp)
        return ''
    
    @property
    def last_update_time(self) -> str:
        """最后更新时间"""
        timestamp = self._card.get('last_update_time', 0) or self._card.get('lastUpdateTime', 0)
        if timestamp:
            return self._convert_timestamp(timestamp)
        return ''
    
    @staticmethod
    def _convert_timestamp(timestamp: int) -> str:
        """转换时间戳"""
        try:
            # 小红书时间戳是毫秒级
            dt = datetime.fromtimestamp(timestamp / 1000)
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ''
    
    @property
    def user_id(self) -> str:
        user = self._card.get('user', {})
        return user.get('user_id', '') or user.get('userId', '')
    
    @property
    def user_nickname(self) -> str:
        user = self._card.get('user', {})
        return user.get('nickname', '')
    
    @property
    def user_avatar(self) -> str:
        user = self._card.get('user', {})
        return user.get('avatar', '')
    
    @property
    def ip_location(self) -> str:
        return self._card.get('ip_location', '') or self._card.get('ipLocation', '')
    
    # 互动信息
    @property
    def liked_count(self) -> int:
        interact = self._card.get('interact_info', {}) or self._card.get('interactInfo', {})
        return self._convert_count(interact.get('liked_count', 0) or interact.get('likedCount', 0))
    
    @property
    def collected_count(self) -> int:
        interact = self._card.get('interact_info', {}) or self._card.get('interactInfo', {})
        return self._convert_count(interact.get('collected_count', 0) or interact.get('collectedCount', 0))
    
    @property
    def comment_count(self) -> int:
        interact = self._card.get('interact_info', {}) or self._card.get('interactInfo', {})
        return self._convert_count(interact.get('comment_count', 0) or interact.get('commentCount', 0))
    
    @property
    def share_count(self) -> int:
        interact = self._card.get('interact_info', {}) or self._card.get('interactInfo', {})
        return self._convert_count(interact.get('share_count', 0) or interact.get('shareCount', 0))
    
    @staticmethod
    def _convert_count(value) -> int:
        """转换数量 (处理 '2.3万' 这种格式)"""
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            if '万' in value:
                return int(float(value.replace('万', '')) * 10000)
            try:
                return int(value)
            except:
                return 0
        return 0
    
    @property
    def image_list(self) -> List[dict]:
        """图片列表"""
        # API: image_list / info_list, 网页端: imageList / infoList
        images = self._card.get('image_list', []) or self._card.get('imageList', [])
        result = []
        for img in images:
            info_list = img.get('info_list', []) or img.get('infoList', [])
            url = img.get('url', '') or img.get('urlDefault', '')
            if info_list:
                # 取最大尺寸的图片
                best = info_list[-1]
                img_url = best.get('url', '') or url
                result.append({
                    'url': img_url,
                    'width': best.get('width', 0) or img.get('width', 0),
                    'height': best.get('height', 0) or img.get('height', 0),
                })
            elif url:
                result.append({
                    'url': url,
                    'width': img.get('width', 0),
                    'height': img.get('height', 0),
                })
        return result
    
    @property
    def video_url(self) -> str:
        """视频 URL"""
        video = self._card.get('video', {})
        if not video:
            return ''
        
        # API 格式: video.media.stream.h264[0].master_url
        media = video.get('media', {})
        if media:
            stream = media.get('stream', {})
            h264 = stream.get('h264', [])
            if h264:
                return h264[0].get('master_url', '') or h264[0].get('backup_urls', [''])[0]
        
        # 网页端格式: video.media.stream.h264[0].master_url 或 video.consumer.originVideoKey
        if media:
            stream = media.get('stream', {})
            for key in ['h264', 'h265', 'av1']:
                streams = stream.get(key, [])
                if streams:
                    return streams[0].get('master_url', '') or streams[0].get('backup_urls', [''])[0]
        
        # 备用：直接从 video 中提取
        origin_key = video.get('consumer', {}).get('originVideoKey', '')
        if origin_key:
            return origin_key
        
        return ''
    
    def to_dict(self) -> dict:
        return {
            'note_id': self.note_id,
            'xsec_token': self.xsec_token,
            'note_url': self.note_url,
            'model_type': self.model_type,
            'title': self.title,
            'desc': self.desc,
            'tags': self.tags,
            'publish_time': self.publish_time,
            'user_id': self.user_id,
            'user_nickname': self.user_nickname,
            'user_avatar': self.user_avatar,
            'ip_location': self.ip_location,
            'liked_count': self.liked_count,
            'collected_count': self.collected_count,
            'comment_count': self.comment_count,
            'share_count': self.share_count,
            'image_list': self.image_list,
            'video_url': self.video_url,
        }


class UserPostedFilter:
    """用户笔记列表过滤器"""
    
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('data', {})
    
    @property
    def success(self) -> bool:
        return self.raw.get('success', False)
    
    @property
    def has_more(self) -> bool:
        return self._data.get('has_more', False)
    
    @property
    def cursor(self) -> str:
        return self._data.get('cursor', '')
    
    @property
    def notes(self) -> List[dict]:
        """笔记列表"""
        notes = self._data.get('notes', [])
        return [NoteCardFilter(n).to_dict() for n in notes]
    
    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'has_more': self.has_more,
            'cursor': self.cursor,
            'notes': self.notes,
        }


class SearchFilter:
    """搜索结果过滤器"""
    
    def __init__(self, data: dict):
        self.raw = data
        self._data = data.get('data', {})
    
    @property
    def success(self) -> bool:
        return self.raw.get('success', False)
    
    @property
    def has_more(self) -> bool:
        return self._data.get('has_more', False)
    
    @property
    def cursor(self) -> str:
        return self._data.get('cursor', '')
    
    @property
    def items(self) -> List[dict]:
        """搜索结果列表"""
        items = self._data.get('items', [])
        result = []
        for item in items:
            if 'note_card' in item:
                result.append(NoteCardFilter(item).to_dict())
        return result
    
    def to_dict(self) -> dict:
        return {
            'success': self.success,
            'has_more': self.has_more,
            'cursor': self.cursor,
            'items': self.items,
        }
