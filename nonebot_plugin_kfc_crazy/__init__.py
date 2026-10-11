import json
import random
from pathlib import Path

from nonebot import get_bots, get_plugin_config, logger, on_fullmatch, require
from nonebot.adapters.onebot.v11 import Bot, MessageSegment
from nonebot.matcher import Matcher
from nonebot.plugin import PluginMetadata

from .config import Config

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

config = get_plugin_config(Config)

__plugin_meta__ = PluginMetadata(
    name="疯狂星期四",
    description="随机发送疯狂星期四语录，每周四上午 10 点自动发送语录。",
    usage="发送“疯狂星期四”获取随机语录；配置kfc_crazy_group_ids开启定时群发送。",
    type="application",
    homepage="https://github.com/HuParry/nonebot-plugin-kfc-crazy",
    config=Config,
    supported_adapters={"~onebot.v11"},
)

crazy_thursday = on_fullmatch("疯狂星期四", priority=15, block=True)


def random_kfc() -> str:
    with (Path(__file__).parent / "post.json").open(encoding="utf-8") as f:
        posts = json.load(f).get("post", None)
        if posts is None:
            raise KeyError("Key 'post' is missing.")

    return random.choice(posts).replace("thursday", "Thursday")


@crazy_thursday.handle()
async def send_random_post(matcher: Matcher):
    await matcher.finish(MessageSegment.text(random_kfc()))


@scheduler.scheduled_job(
    "cron",
    day_of_week="thu",
    hour=10,
    minute=0,
    second=0,
    timezone="Asia/Shanghai",
    id="crazy_thursday_weekly_post",
)
async def send_weekly_post():
    if not config.kfc_crazy_group_ids:
        return

    for bot in get_bots().values():
        if not isinstance(bot, Bot):
            continue
        for group_id in sorted(config.kfc_crazy_group_ids):
            try:
                await bot.send_group_msg(
                    group_id=group_id,
                    message=MessageSegment.text(random_kfc()),
                )
            except Exception:
                logger.exception(
                    f"疯狂星期四语录发送失败：Bot {bot.self_id}，群 {group_id}"
                )
