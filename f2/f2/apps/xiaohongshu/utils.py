# path: f2/apps/xiaohongshu/utils.py

"""
小红书平台签名生成工具
Xiaohongshu Signature Generator

核心签名参数:
- x-s: 核心加密签名
- x-t: 时间戳签名
- xsec_token: 安全令牌
"""

import time
import hashlib
import json
import re
from typing import Optional, Dict, Any, List

from f2.log.logger import logger


class XhsSignatureManager:
    """小红书签名管理器"""
    
    def __init__(self):
        self._js_context = None
    
    def _load_js_sign(self):
        """加载 JS 签名文件"""
        try:
            import execjs
            js_code = """
            function getXs(e, t, n) {
                var i = Date.now().toString();
                var r = [e, JSON.stringify(t || {}), n, i].join("");
                var o = md5(r);
                return {
                    'X-s': o,
                    'X-t': i
                };
            }
            
            function md5(e) {
                function r(e, r) {
                    var t = (65535 & e) + (65535 & r);
                    return (e >> 16) + (r >> 16) + (t >> 16) << 16 | 65535 & t
                }

                function t(e) {
                    for (var t, n = e.length, i = n + 8, o = (i - (i % 64)) / 64 + 1, a = new Array(16 * o), s = 0; s < n; s++)
                        a[s >> 2] |= e.charCodeAt(s) << (8 * (s % 4));
                    a[i >> 2] |= 128 << (8 * (i % 4));
                    a[16 * o - 1] = 8 * n;
                    var c, u, f, d, h, p, v, g, y = 1732584193, m = 4023233417, _ = 2562383102, b = 271733878, w = [7, 12, 17, 22, 5, 9, 14, 20, 4, 11, 16, 23, 6, 10, 15, 21];

                    function x(e) {
                        return e >>> 0
                    }

                    function S(e) {
                        var t, n, i;
                        e = x(e);
                        t = e & 255;
                        n = e >> 8 & 255;
                        i = e >> 16 & 255;
                        return String.fromCharCode(t) + String.fromCharCode(n) + String.fromCharCode(i) + String.fromCharCode(e >> 24 & 255)
                    }

                    function C(e) {
                        return x((e << 7) | (e >>> 25))
                    }

                    function k(e) {
                        return x((e << 12) | (e >>> 20))
                    }

                    function A(e) {
                        return x((e << 17) | (e >>> 15))
                    }

                    function O(e) {
                        return x((e << 22) | (e >>> 10))
                    }

                    function R(e) {
                        return x((e >>> 7) | (e << 25))
                    }

                    function E(e) {
                        return x((e >>> 12) | (e << 20))
                    }

                    function M(e) {
                        return x((e >>> 17) | (e << 15))
                    }

                    function T(e) {
                        return x((e >>> 22) | (e << 10))
                    }

                    function N(e, t, n, i, o, a, s) {
                        return r(R(r(r(t, e), r(i, s))), a)
                    }

                    function j(e, t, n, i, o, a, s) {
                        return r(M(r(r(i, e), r(t, s))), a)
                    }

                    function L(e, t, n, i, o, a, s) {
                        return r(T(r(r(t & n | ~t & i, e), r(o, s))), a)
                    }

                    function P(e, t, n, i, o, a, s) {
                        return r(A(r(r(t ^ n ^ i, e), r(o, s))), a)
                    }

                    function D(e, t, n, i, o, a, s) {
                        return r(O(r(r(n ^ (t | ~i), e), r(o, s))), a)
                    }

                    for (c = 0; c < a.length; c += 16) {
                        u = y;
                        f = m;
                        d = _;
                        h = b;
                        y = N(y, m, _, b, a[c + 0], w[0], 3614090360);
                        b = N(b, y, m, _, a[c + 1], w[1], 3905402710);
                        _ = N(_, b, y, m, a[c + 2], w[2], 606105819);
                        m = N(m, _, b, y, a[c + 3], w[3], 3250441966);
                        y = N(y, m, _, b, a[c + 4], w[4], 4118548399);
                        b = N(b, y, m, _, a[c + 5], w[5], 1200080426);
                        _ = N(_, b, y, m, a[c + 6], w[6], 2821735955);
                        m = N(m, _, b, y, a[c + 7], w[7], 4249261313);
                        y = j(y, m, _, b, a[c + 8], w[8], 1770035416);
                        b = j(b, y, m, _, a[c + 9], w[9], 2336552879);
                        _ = j(_, b, y, m, a[c + 10], w[10], 4294925233);
                        m = j(m, _, b, y, a[c + 11], w[11], 2304563134);
                        y = j(y, m, _, b, a[c + 12], w[12], 1804603682);
                        b = j(b, y, m, _, a[c + 13], w[13], 4254626195);
                        _ = j(_, b, y, m, a[c + 14], w[14], 2792965006);
                        m = j(m, _, b, y, a[c + 15], w[15], 1236535329);
                        y = L(y, m, _, b, a[c + 1], w[0], 4129170786);
                        b = L(b, y, m, _, a[c + 6], w[1], 3225465664);
                        _ = L(_, b, y, m, a[c + 11], w[2], 643717713);
                        m = L(m, _, b, y, a[c + 0], w[3], 3921069994);
                        y = L(y, m, _, b, a[c + 5], w[4], 3593408605);
                        b = L(b, y, m, _, a[c + 10], w[5], 38016083);
                        _ = L(_, b, y, m, a[c + 15], w[6], 3634488961);
                        m = L(m, _, b, y, a[c + 4], w[7], 3889429448);
                        y = P(y, m, _, b, a[c + 9], w[8], 568446438);
                        b = P(b, y, m, _, a[c + 14], w[9], 3275163606);
                        _ = P(_, b, y, m, a[c + 3], w[10], 4107603335);
                        m = P(m, _, b, y, a[c + 8], w[11], 1163531501);
                        y = P(y, m, _, b, a[c + 13], w[12], 2850285829);
                        b = P(b, y, m, _, a[c + 2], w[13], 4243563512);
                        _ = P(_, b, y, m, a[c + 7], w[14], 1735328473);
                        m = P(m, _, b, y, a[c + 12], w[15], 2368359562);
                        y = D(y, m, _, b, a[c + 5], w[0], 4294588738);
                        b = D(b, y, m, _, a[c + 8], w[1], 2272392833);
                        _ = D(_, b, y, m, a[c + 11], w[2], 1839030562);
                        m = D(m, _, b, y, a[c + 14], w[3], 4259657740);
                        y = D(y, m, _, b, a[c + 1], w[4], 2763975236);
                        b = D(b, y, m, _, a[c + 4], w[5], 1272893353);
                        _ = D(_, b, y, m, a[c + 7], w[6], 4139469664);
                        m = D(m, _, b, y, a[c + 10], w[7], 3200236656);
                        y = D(y, m, _, b, a[c + 13], w[8], 681279174);
                        b = D(b, y, m, _, a[c + 0], w[9], 3936430074);
                        _ = D(_, b, y, m, a[c + 3], w[10], 3572445317);
                        m = D(m, _, b, y, a[c + 6], w[11], 76029189);
                        y = D(y, m, _, b, a[c + 9], w[12], 3654602809);
                        b = D(b, y, m, _, a[c + 12], w[13], 3873151461);
                        _ = D(_, b, y, m, a[c + 15], w[14], 530742520);
                        m = D(m, _, b, y, a[c + 2], w[15], 3299628645);
                        y = r(y, u);
                        m = r(m, f);
                        _ = r(_, d);
                        b = r(b, h)
                    }
                    return S(y) + S(m) + S(_) + S(b)
                }
            }
            """
            self._js_context = execjs.compile(js_code)
        except Exception as e:
            print(f"Warning: Could not load JS sign: {e}")
            self._js_context = None
    
    def generate_sign(
        self, 
        api: str, 
        data: Optional[Dict] = None, 
        a1: str = ""
    ) -> Dict[str, str]:
        """
        生成 x-s 和 x-t 签名
        
        Args:
            api: API 路径
            data: 请求数据
            a1: Cookie 中的 a1 值
            
        Returns:
            {'x-s': '...', 'x-t': '...'}
        """
        if self._js_context:
            try:
                sign = self._js_context.call('getXs', api, data, a1)
                return {
                    'x-s': sign['X-s'],
                    'x-t': str(sign['X-t'])
                }
            except Exception as e:
                print(f"JS sign error: {e}")
        
        return self._generate_simple_sign(api, data, a1)
    
    def _generate_simple_sign(
        self, 
        api: str, 
        data: Optional[Dict] = None, 
        a1: str = ""
    ) -> Dict[str, str]:
        """简化签名生成 (使用MD5)"""
        timestamp = int(time.time() * 1000)
        sign_str = f"{api}{json.dumps(data or {}, separators=(',', ':'))}{a1}{timestamp}"
        
        x_s = hashlib.md5(sign_str.encode()).hexdigest()
        
        return {
            'x-s': x_s,
            'x-t': str(timestamp)
        }


class XsecTokenManager:
    """xsec_token 管理器"""
    
    @staticmethod
    def extract_from_response(response_data: dict) -> str:
        """从响应中提取 xsec_token"""
        if isinstance(response_data, dict):
            if 'data' in response_data:
                data = response_data['data']
                if 'notes' in data and data['notes']:
                    return data['notes'][0].get('xsec_token', '')
            if 'xsec_token' in response_data:
                return response_data['xsec_token']
        return ''


class ClientConfManager:
    """小红书客户端配置管理"""
    
    DEFAULT_HEADERS = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.xiaohongshu.com",
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    
    @classmethod
    def get_headers(cls, cookie: str = "") -> dict:
        """获取请求头"""
        headers = cls.DEFAULT_HEADERS.copy()
        if cookie:
            headers["cookie"] = cookie
        return headers
    
    @classmethod
    def get_a1_from_cookie(cls, cookie: str) -> str:
        """从 Cookie 中提取 a1 值"""
        if not cookie:
            return ""
        
        for item in cookie.split(';'):
            item = item.strip()
            if item.startswith('a1='):
                return item[3:]
        return ""


class NoteIdFetcher:
    """笔记 ID 提取器"""
    
    @staticmethod
    def _resolve_short_url(url: str) -> str:
        """
        解析短链接，跟随重定向获取真实 URL
        
        支持:
        - https://xhslink.com/xxxxx
        - http://xhslink.com/xxxxx (自动转为 https)
        - https://xhslink.com/o/xxxxx
        """
        if 'xhslink.com' not in url:
            return url
        
        # 确保 https
        if url.startswith('http://'):
            url = 'https://' + url[7:]
        
        try:
            import requests as req
            resp = req.head(url, allow_redirects=True, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
            })
            resolved = resp.url
            # 如果 head 方法没有跟随重定向(某些服务器不支持HEAD)，尝试GET
            if 'xhslink.com' in resolved:
                resp = req.get(url, allow_redirects=True, timeout=15, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
                })
                resolved = resp.url
            return resolved
        except Exception as e:
            logger.warning(f"解析短链接失败: {e}")
            return url
    
    @staticmethod
    def get_note_id(url: str) -> str:
        """
        从 URL 提取笔记 ID
        
        支持格式:
        - https://www.xiaohongshu.com/explore/xxxxx
        - https://www.xiaohongshu.com/discovery/item/xxxxx
        - https://www.xiaohongshu.com/search_result/xxxxx
        - https://xhslink.com/xxxxx (短链，自动解析)
        - https://xhslink.com/o/xxxxx (短链，自动解析)
        - 直接输入笔记 ID
        """
        # 如果是短链接，先解析获取真实 URL
        if 'xhslink.com' in url:
            url = NoteIdFetcher._resolve_short_url(url)
        
        # 匹配 /explore/xxxxx
        match = re.search(r'/explore/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        
        # 匹配 /discovery/item/xxxxx
        match = re.search(r'/discovery/item/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        
        # 匹配 /search_result/xxxxx
        match = re.search(r'/search_result/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        
        # 匹配 note_id=xxxxx 参数
        match = re.search(r'note_id=([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        
        # 直接输入笔记 ID (24位十六进制)
        if re.match(r'^[a-f0-9]{24}$', url):
            return url
        
        # 兼容旧格式
        if re.match(r'^[a-zA-Z0-9]{20,}$', url):
            return url
        
        return ""
    
    @staticmethod
    def get_xsec_token(url: str) -> str:
        """
        从 URL 提取 xsec_token
        
        支持格式:
        - https://www.xiaohongshu.com/explore/xxxxx?xsec_token=yyyy
        - 从短链接解析后的真实 URL
        """
        # 如果是短链接，先解析
        if 'xhslink.com' in url:
            url = NoteIdFetcher._resolve_short_url(url)
        
        match = re.search(r'xsec_token=([^&]+)', url)
        if match:
            return match.group(1)
        
        return ""
    
    @staticmethod
    def fetch_note_from_web(url: str, cookie: str = "") -> dict:
        """
        通过网页 HTML 解析获取笔记信息（不依赖签名 API）
        
        当 Cookie 模式的 API 签名失效时，作为备选方案
        直接请求网页版小红书，从 HTML 中提取笔记数据
        
        Args:
            url: 笔记完整 URL (如 https://www.xiaohongshu.com/explore/xxxxx)
            cookie: 小红书 Cookie
            
        Returns:
            笔记数据字典
        """
        import requests as req
        
        # 确保是完整 URL
        if 'xhslink.com' in url:
            url = NoteIdFetcher._resolve_short_url(url)
        
        note_id = NoteIdFetcher.get_note_id(url)
        xsec_token = NoteIdFetcher.get_xsec_token(url)
        
        if not note_id:
            return {}
        
        # 构造网页 URL
        web_url = f"https://www.xiaohongshu.com/explore/{note_id}"
        if xsec_token:
            web_url += f"?xsec_token={xsec_token}&xsec_source=pc_feed"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.xiaohongshu.com/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        if cookie:
            headers['Cookie'] = cookie
        
        try:
            resp = req.get(web_url, headers=headers, timeout=15)
            if resp.status_code != 200:
                return {}
            
            html = resp.text
            
            # 从 HTML 中提取 __INITIAL_STATE__ JSON 数据
            match = re.search(r'window\.__INITIAL_STATE__\s*=\s*({.+?})\s*</script>', html, re.DOTALL)
            if not match:
                match = re.search(r'window\.__INITIAL_STATE__\s*=\s*(.+?)\s*</script>', html, re.DOTALL)
            
            if match:
                import json
                # 小红书的 JSON 中有 undefined 需要替换
                json_str = match.group(1)
                json_str = json_str.replace('undefined', 'null')
                
                try:
                    initial_state = json.loads(json_str)
                except json.JSONDecodeError:
                    # 尝试更宽松的解析
                    try:
                        # 移除末尾的分号等
                        json_str = json_str.rstrip(';')
                        initial_state = json.loads(json_str)
                    except:
                        return {}
                
                # 提取笔记数据
                note_data = initial_state.get('note', {}).get('noteDetailMap', {})
                
                if note_data:
                    # 获取第一个笔记的详情
                    for key, detail in note_data.items():
                        note = detail.get('note', {})
                        if note:
                            return {'note_card': note, 'id': note.get('noteId', note_id), 'xsec_token': xsec_token}
                
                return {}
            
            return {}
            
        except Exception as e:
            logger.warning(f"网页解析失败: {e}")
            return {}
    
    @staticmethod
    def get_all_note_id(urls: List[str]) -> List[str]:
        """批量提取笔记 ID"""
        return [NoteIdFetcher.get_note_id(url) for url in urls]


class UserIdFetcher:
    """用户 ID 提取器"""
    
    @staticmethod
    def get_user_id(url: str) -> str:
        """
        从 URL 提取用户 ID
        
        支持格式:
        - https://www.xiaohongshu.com/user/profile/xxxxx
        - 直接输入用户 ID
        """
        match = re.search(r'/user/profile/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1)
        
        if re.match(r'^[a-zA-Z0-9]{20,}$', url):
            return url
        
        return ""
    
    @staticmethod
    def get_all_user_id(urls: List[str]) -> List[str]:
        """批量提取用户 ID"""
        return [UserIdFetcher.get_user_id(url) for url in urls]


signature_manager = XhsSignatureManager()