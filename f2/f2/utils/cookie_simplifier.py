"""
Cookie 简化工具
自动识别并提取各平台 Cookie 的核心字段
"""

class CookieSimplifier:
    """Cookie 简化器"""

    DOUYIN_CORE_FIELDS = [
        'sessionid', 'sessionid_ss', 'sid_tt', 'uid_tt', 'uid_tt_ss',
        'sid_guard', 'ttwid', 'passport_csrf_token', 's_v_web_id', 'odin_tt',
        'sid_ucp_v1', 'ssid_ucp_v1', 'session_tlb_tag', 'biz_trace_id'
    ]

    XIAOHONGSHU_CORE_FIELDS = [
        'a1', 'web_session', 'webId', 'webBuild', 'xsecappid',
        'websectiga', 'ets', 'abRequestId', 'unread', 'sec_poison_id',
        'x-rednote-datactry', 'x-rednote-holderctry', 'loadts'
    ]

    WEIBO_CORE_FIELDS = [
        'ALF', 'MLOGIN', 'SCF', 'SUB', '_T_WM', 'WBPSESS', 'login',
        'SUS', 'SUP', 'UGSETN', 'WBREF', 'weibo_rogue', 'wvr', 'SSOLoginState'
    ]

    @staticmethod
    def parse_cookie_string(cookie_str: str) -> dict:
        """
        将 Cookie 字符串解析为字典

        Args:
            cookie_str: Cookie 字符串，格式为 "key1=value1; key2=value2"

        Returns:
            Cookie 字典
        """
        if not cookie_str:
            return {}

        cookie_dict = {}
        cookie_str = cookie_str.strip()

        if cookie_str.startswith('{') or cookie_str.startswith('"'):
            import json
            try:
                data = json.loads(cookie_str)
                if isinstance(data, dict) and 'cookie' in data:
                    cookie_str = data['cookie']
                elif isinstance(data, dict):
                    return data
            except:
                pass

        pairs = cookie_str.split(';')
        for pair in pairs:
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split('=', 1)
                key = key.strip()
                value = value.strip()
                if key and value:
                    cookie_dict[key] = value

        return cookie_dict

    @staticmethod
    def simplify_cookie(cookie_str: str, platform: str) -> str:
        """
        简化 Cookie，只保留核心字段

        Args:
            cookie_str: 原始 Cookie 字符串
            platform: 平台名称 (douyin/xiaohongshu/weibo)

        Returns:
            简化后的 Cookie 字符串
        """
        cookie_dict = CookieSimplifier.parse_cookie_string(cookie_str)

        if not cookie_dict:
            return cookie_str

        if platform == 'douyin':
            core_fields = CookieSimplifier.DOUYIN_CORE_FIELDS
        elif platform == 'xiaohongshu':
            core_fields = CookieSimplifier.XIAOHONGSHU_CORE_FIELDS
        elif platform == 'weibo':
            core_fields = CookieSimplifier.WEIBO_CORE_FIELDS
        else:
            return cookie_str

        simplified = {}
        for field in core_fields:
            if field in cookie_dict:
                simplified[field] = cookie_dict[field]

        for key, value in cookie_dict.items():
            if key not in simplified and len(value) < 200:
                simplified[key] = value

        cookie_pairs = [f"{k}={v}" for k, v in simplified.items()]
        return '; '.join(cookie_pairs)

    @staticmethod
    def detect_platform(cookie_str: str) -> str:
        """
        根据 Cookie 内容检测平台

        Args:
            cookie_str: Cookie 字符串

        Returns:
            平台名称
        """
        cookie_dict = CookieSimplifier.parse_cookie_string(cookie_str)

        if not cookie_dict:
            return 'unknown'

        if any(key in cookie_dict for key in ['sid_tt', 'sessionid', 'ttwid', 'douyin.com']):
            return 'douyin'
        elif any(key in cookie_dict for key in ['a1', 'web_session', 'xhs', 'xiaohongshu']):
            return 'xiaohongshu'
        elif any(key in cookie_dict for key in ['SUB', '_T_WM', 'weibo', 'WBPSESS']):
            return 'weibo'

        return 'unknown'

    @staticmethod
    def validate_cookie(cookie_str: str, platform: str) -> dict:
        """
        验证 Cookie 是否有效

        Args:
            cookie_str: Cookie 字符串
            platform: 平台名称

        Returns:
            验证结果字典
        """
        cookie_dict = CookieSimplifier.parse_cookie_string(cookie_str)

        if not cookie_dict:
            return {
                'valid': False,
                'message': 'Cookie 为空',
                'core_fields_found': 0,
                'total_fields': 0
            }

        if platform == 'douyin':
            required = ['sessionid', 'sid_tt']
        elif platform == 'xiaohongshu':
            required = ['a1', 'web_session']
        elif platform == 'weibo':
            required = ['SUB']
        else:
            required = []

        missing = [field for field in required if field not in cookie_dict]

        if missing:
            return {
                'valid': False,
                'message': f'缺少必需字段: {", ".join(missing)}',
                'core_fields_found': len([f for f in required if f in cookie_dict]),
                'total_fields': len(cookie_dict)
            }

        return {
            'valid': True,
            'message': 'Cookie 有效',
            'core_fields_found': len(cookie_dict),
            'total_fields': len(cookie_dict)
        }


cookie_simplifier = CookieSimplifier()
