# path: f2/apps/douyin/cli.py

import f2
import click
import typing
import traceback

from pathlib import Path

from f2 import helps
from f2.cli.cli_commands import set_cli_config
from f2.log.logger import logger, trace_logger
from f2.utils.utils import (
    split_dict_cookie,
    get_resource_path,
    get_cookie_from_browser,
    check_invalid_naming,
    merge_config,
    check_proxy_avail,
)
from f2.utils.conf_manager import ConfigManager
from f2.i18n.translator import TranslationManager, _

from f2.apps.douyin.utils import ClientConfManager, VideoIdFetcher


def handler_help(
    ctx: click.Context,
    param: typing.Union[click.Option, click.Parameter],
    value: typing.Any,
) -> None:
    if not value or ctx.resilient_parsing:
        return
    get_help("douyin")
    ctx.exit()


def handler_auto_cookie(
    ctx: click.Context,
    param: typing.Union[click.Option, click.Parameter],
    value: typing.Any,
) -> None:
    if not value or ctx.resilient_parsing or ctx.params.get("cookie"):
        return

    try:
        cookie_value = split_dict_cookie(get_cookie_from_browser(value, "douyin.com"))

        if not cookie_value:
            raise ValueError(_("无法从 {0} 浏览器中获取cookie").format(value))

        manager = ConfigManager(
            ctx.params.get("config", get_resource_path(f2.APP_CONFIG_FILE_PATH))
        )
        manager.update_config_with_args("douyin", cookie=cookie_value)
    except PermissionError:
        logger.error(_("请结束所有浏览器相关的进程，并确保你有管理员的权限访问浏览器后重试！"))
        ctx.abort()
    except Exception as e:
        trace_logger.error(traceback.format_exc())
        logger.error(_("自动获取Cookie失败：{0}").format(str(e)))
        ctx.abort()
    finally:
        ctx.exit(0)


def handler_naming(
    ctx: click.Context,
    param: typing.Union[click.Option, click.Parameter],
    value: typing.Any,
) -> typing.Any:
    if not value or ctx.resilient_parsing:
        return

    ALLOWED_PATTERNS = [
        "{aweme_id}",
        "{title}",
        "{desc}",
        "{nickname}",
        "{user_id}",
        "{create}",
        "{type}",
    ]

    invalid_patterns = check_invalid_naming(value, ALLOWED_PATTERNS)
    if invalid_patterns:
        logger.error(
            _("命名模板包含非法字段: {0}").format(invalid_patterns)
        )
        logger.info(_("可用字段: {0}").format(ALLOWED_PATTERNS))
        ctx.abort()

    return value


@click.command(name="douyin", help=_("抖音视频解析下载"))
@click.option(
    "--config",
    "-c",
    type=click.Path(file_okay=True, dir_okay=False, readable=True, resolve_path=True),
    default=get_resource_path(f2.APP_CONFIG_FILE_PATH),
    help=_("配置文件路径"),
)
@click.option(
    "--url",
    "-u",
    type=str,
    default="",
    help=_("视频链接或用户主页链接"),
)
@click.option(
    "--mode",
    "-M",
    type=click.Choice(["one", "post", "search"]),
    default="one",
    help=_("下载模式: one(单个视频), post(用户视频), search(搜索)"),
)
@click.option(
    "--api-mode",
    "-am",
    type=click.Choice(["cookie", "tikhub"]),
    default="cookie",
    help=_("API 调用模式: cookie(直接调用抖音API), tikhub(使用TikHub API)"),
)
@click.option(
    "--cookie",
    "-k",
    type=str,
    default="",
    help=_("抖音 Cookie (cookie 模式使用)"),
)
@click.option(
    "--tikhub-api-key",
    "-tk",
    type=str,
    default="",
    help=_("TikHub API Key (tikhub 模式使用)"),
)
@click.option(
    "--auto-cookie",
    "-a",
    type=click.Choice(f2.BROWSER_LIST),
    default="",
    callback=handler_auto_cookie,
    is_eager=True,
    help=_("自动从浏览器获取 Cookie"),
)
@click.option(
    "--naming",
    "-n",
    type=str,
    default="{create}_{title}",
    callback=handler_naming,
    help=_("文件命名模板"),
)
@click.option(
    "--path",
    "-p",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    default="Download",
    help=_("下载保存路径"),
)
@click.option(
    "--timeout",
    "-t",
    type=int,
    default=10,
    help=_("请求超时时间(秒)"),
)
@click.option(
    "--max-retries",
    "-r",
    type=int,
    default=3,
    help=_("最大重试次数"),
)
@click.option(
    "--max-tasks",
    "-m",
    type=int,
    default=10,
    help=_("最大并发任务数"),
)
@click.option(
    "--download",
    "-d",
    type=bool,
    default=True,
    help=_("是否下载文件"),
)
@click.option(
    "--cover",
    "-cv",
    type=bool,
    default=True,
    help=_("是否下载封面"),
)
@click.option(
    "--desc",
    "-dc",
    type=bool,
    default=True,
    help=_("是否保存文案"),
)
@click.option(
    "--proxy",
    "-pr",
    type=str,
    default="",
    callback=lambda ctx, param, value: check_proxy_avail(value),
    help=_("代理地址"),
)
@click.option(
    "--language",
    "-l",
    type=click.Choice(["zh_CN", "en_US"]),
    default="zh_CN",
    callback=lambda ctx, param, value: TranslationManager.set_language(value) or value,
    is_eager=True,
    help=_("语言设置"),
)
@click.option(
    "--help",
    "-h",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=handler_help,
    help=_("显示帮助信息"),
)
@click.pass_context
def douyin(ctx: click.Context, **kwargs):
    main_conf = ConfigManager(kwargs.get("config")).get_config("douyin")
    custom_conf = kwargs
    kwargs = merge_config(main_conf, custom_conf)
    kwargs["app_name"] = "douyin"
    ctx.invoke(set_cli_config, **kwargs)


def get_help(app_name: str) -> None:
    from f2.apps.douyin.help import get_help as get_douyin_help
    get_douyin_help()

from f2.apps.douyin.help import get_help