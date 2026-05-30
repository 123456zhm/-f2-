# path: f2/apps/xiaohongshu/__init__.py

from f2.apps.xiaohongshu.api import XiaohongshuAPIEndpoints, XiaohongshuHeaders
from f2.apps.xiaohongshu.model import (
    BaseRequestModel,
    UserProfileRequest,
    UserPostedRequest,
    NoteDetailRequest,
    SearchNotesRequest,
    UserInfo,
    NoteCard,
    NoteDetail,
)
from f2.apps.xiaohongshu.utils import (
    XhsSignatureManager,
    XsecTokenManager,
    ClientConfManager,
    NoteIdFetcher,
    UserIdFetcher,
    signature_manager,
)
from f2.apps.xiaohongshu.crawler import XiaohongshuCrawler
from f2.apps.xiaohongshu.filter import (
    UserProfileFilter,
    NoteCardFilter,
    UserPostedFilter,
    SearchFilter,
)
from f2.apps.xiaohongshu.handler import (
    XiaohongshuHandler,
    get_note_detail,
    get_user_notes,
    search_notes,
)
from f2.apps.xiaohongshu.dl import XiaohongshuDownloader

__all__ = [
    # API
    "XiaohongshuAPIEndpoints",
    "XiaohongshuHeaders",
    
    # Models
    "BaseRequestModel",
    "UserProfileRequest",
    "UserPostedRequest",
    "NoteDetailRequest",
    "SearchNotesRequest",
    "UserInfo",
    "NoteCard",
    "NoteDetail",
    
    # Utils
    "XhsSignatureManager",
    "XsecTokenManager",
    "ClientConfManager",
    "NoteIdFetcher",
    "UserIdFetcher",
    "signature_manager",
    
    # Core
    "XiaohongshuCrawler",
    "XiaohongshuHandler",
    "XiaohongshuDownloader",
    
    # Filters
    "UserProfileFilter",
    "NoteCardFilter",
    "UserPostedFilter",
    "SearchFilter",
    
    # Convenience functions
    "get_note_detail",
    "get_user_notes",
    "search_notes",
]