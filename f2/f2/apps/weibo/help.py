# path: f2/apps/weibo/help.py

from f2.i18n.translator import _
from f2.log.logger import logger


def get_help() -> None:
    help_text = """
╭──────────────────────────────────────────────────────────────────────────────────────────╮
│                              微博 (Weibo)                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────╯

用法: f2 weibo [选项]

选项:
  -u, --url          微博链接或用户主页链接
  -M, --mode         下载模式:
                      • one    - 单条微博解析下载
                      • post   - 用户发布的微博列表
                      • search - 搜索微博
  -c, --config       配置文件路径 (默认: conf/app.yaml)
  -k, --cookie       微博 Cookie
  -a, --auto-cookie  自动从浏览器获取 Cookie (chrome/firefox/edge等)
  -n, --naming       文件命名模板 (默认: {create}_{title})
                      可用字段: {status_id}, {title}, {desc}, {nickname}, {user_id}, {create}, {type}
  -p, --path         下载保存路径 (默认: Download)
  -t, --timeout      请求超时时间 (默认: 10秒)
  -r, --max-retries  最大重试次数 (默认: 3)
  -m, --max-tasks    最大并发任务数 (默认: 10)
  -d, --download     是否下载文件 (默认: True)
  -cv, --cover       是否下载封面 (默认: True)
  -dc, --desc        是否保存文案 (默认: True)
  -pr, --proxy       代理地址
  -l, --language     语言设置 (zh_CN/en_US)
  -h, --help         显示帮助信息

示例:
  # 解析单条微博
  f2 weibo -u https://weibo.com/123456789/abc123456789
  
  # 批量下载用户微博
  f2 weibo -u https://weibo.com/u/123456789 -M post
  
  # 搜索微博
  f2 weibo -M search -u "热点新闻"
  
  # 使用自动 Cookie
  f2 weibo -u https://weibo.com/123456789/abc123456789 -a chrome

注意事项:
  1. 部分接口需要登录 Cookie，可使用 -a 自动获取或手动设置 -k
  2. 支持下载微博中的图片和视频

更多信息请访问: https://f2.wiki
"""
    logger.info(help_text)