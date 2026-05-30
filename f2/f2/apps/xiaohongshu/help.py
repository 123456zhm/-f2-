# path: f2/apps/xiaohongshu/help.py

from f2.i18n.translator import _
from f2.log.logger import logger


def get_help(app_name: str) -> None:
    """显示小红书帮助信息"""
    
    help_text = """
╭──────────────────────────────────────────────────────────────────────────────────────────╮
│                              小红书 (Xiaohongshu / Little Red Book)                        │
╰──────────────────────────────────────────────────────────────────────────────────────────╯

用法: f2 xiaohongshu [选项]

选项:
  -u, --url          笔记链接或用户主页链接
  -M, --mode         下载模式:
                      • one    - 单个笔记解析下载
                      • post   - 用户发布的笔记列表
                      • search - 搜索笔记
  -c, --config       配置文件路径 (默认: conf/app.yaml)
  -k, --cookie       小红书 Cookie
  -a, --auto-cookie  自动从浏览器获取 Cookie (chrome/firefox/edge等)
  -n, --naming       文件命名模板 (默认: {create}_{title})
                      可用字段: {note_id}, {title}, {desc}, {nickname}, {user_id}, {create}, {type}
  -p, --path         下载保存路径 (默认: Download)
  -t, --timeout      请求超时时间 (默认: 10秒)
  -r, --max-retries  最大重试次数 (默认: 3)
  -m, --max-tasks    最大并发任务数 (默认: 10)
  -pc, --page-counts 每页笔记数量 (默认: 20)
  -d, --download     是否下载文件 (默认: True)
  -cv, --cover       是否下载封面 (默认: True)
  -dc, --desc        是否保存文案 (默认: True)
  -pr, --proxy       代理地址
  -l, --language     语言设置 (zh_CN/en_US)
  -h, --help         显示帮助信息

示例:
  # 解析单个笔记
  f2 xiaohongshu -u https://www.xiaohongshu.com/explore/65abc123
  
  # 批量下载用户笔记
  f2 xiaohongshu -u https://www.xiaohongshu.com/user/profile/5abc123 -M post
  
  # 搜索笔记
  f2 xiaohongshu -M search -u "穿搭"
  
  # 使用自动 Cookie
  f2 xiaohongshu -u https://www.xiaohongshu.com/explore/65abc123 -a chrome
  
  # 自定义命名和路径
  f2 xiaohongshu -u https://www.xiaohongshu.com/explore/65abc123 -n "{nickname}_{title}" -p ./downloads

注意事项:
  1. 部分接口需要登录 Cookie，可使用 -a 自动获取或手动设置 -k
  2. 签名参数 (x-s, x-t) 需要逆向获取，当前使用简化签名可能无法正常工作
  3. 下载的图片/视频为无水印版本

更多信息请访问: https://f2.wiki
"""
    
    logger.info(help_text)