import asyncio
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from zoneinfo import ZoneInfo

import nonebot
import pytest
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, Message

nonebot.init(driver="~none")
assert nonebot.load_plugin("nonebot_plugin_kfc_crazy") is not None

import nonebot_plugin_kfc_crazy as plugin
from nonebot_plugin_apscheduler import scheduler
from nonebot_plugin_kfc_crazy.config import Config

POSTS = json.loads(
    (Path(plugin.__file__).parent / "post.json").read_text(encoding="utf-8")
)["post"]


@pytest.mark.parametrize("post", POSTS + ["木曜日 Thursday thursday 星期四 周四 礼拜四"])
def test_quote_processing_matches_original_thursday_logic(monkeypatch, post):
    monkeypatch.setattr(plugin.random, "choice", lambda posts: post)
    expected = (
        post.replace("木曜日", "木曜日")
        .replace("Thursday", "Thursday")
        .replace("thursday", "Thursday")
        .replace("星期四", "星期四")
        .replace("周四", "周四")
        .replace("礼拜四", "礼拜四")
    )
    assert plugin.random_kfc() == expected


def test_config_defaults_and_duplicate_groups():
    assert Config().kfc_crazy_group_ids == set()
    assert Config(kfc_crazy_group_ids=[123, "456", 123]).kfc_crazy_group_ids == {
        123,
        456,
    }


@pytest.mark.parametrize(
    ("text", "matches"),
    [
        ("疯狂星期四", True),
        ("疯狂星期一", False),
        ("狂乱木曜日", False),
        ("今天疯狂星期四", False),
        ("疯狂星期四！", False),
    ],
)
def test_only_exact_thursday_message_matches(text, matches):
    event = MagicMock(spec=Event)
    event.get_type.return_value = "message"
    event.get_plaintext.return_value = text
    event.get_message.return_value = Message(text)
    result = asyncio.run(plugin.crazy_thursday.rule(MagicMock(spec=Bot), event, {}))
    assert result is matches


def test_manual_reply_uses_quote(monkeypatch):
    monkeypatch.setattr(plugin, "random_kfc", lambda: "测试语录")
    matcher = MagicMock()
    matcher.finish = AsyncMock()
    asyncio.run(plugin.send_random_post(matcher))
    assert str(matcher.finish.call_args.args[0]) == "测试语录"


def test_next_run_is_thursday_at_ten_in_shanghai():
    job = scheduler.get_job("crazy_thursday_weekly_post")
    timezone = ZoneInfo("Asia/Shanghai")
    now = datetime(2026, 10, 11, 12, tzinfo=timezone)
    next_run = job.trigger.get_next_fire_time(None, now)
    assert next_run == datetime(2026, 10, 15, 10, tzinfo=timezone)
    assert job.trigger.get_next_fire_time(next_run, next_run) == datetime(
        2026, 10, 22, 10, tzinfo=timezone
    )


def test_weekly_send_continues_after_failure_and_skips_other_adapters(monkeypatch):
    bot = MagicMock(spec=Bot)
    bot.self_id = "10000"
    bot.send_group_msg = AsyncMock(side_effect=[RuntimeError("发送失败"), None])
    other_bot = MagicMock()
    monkeypatch.setattr(plugin, "get_bots", lambda: {"qq": bot, "other": other_bot})
    monkeypatch.setattr(plugin, "config", Config(kfc_crazy_group_ids=[123, 456]))
    monkeypatch.setattr(plugin, "random_kfc", lambda: "测试语录")
    asyncio.run(plugin.send_weekly_post())
    assert [call.kwargs["group_id"] for call in bot.send_group_msg.call_args_list] == [
        123,
        456,
    ]
    assert all(
        str(call.kwargs["message"]) == "测试语录"
        for call in bot.send_group_msg.call_args_list
    )
    other_bot.send_group_msg.assert_not_called()


def test_empty_config_sends_nothing(monkeypatch):
    bot = MagicMock(spec=Bot)
    bot.send_group_msg = AsyncMock()
    monkeypatch.setattr(plugin, "get_bots", lambda: {"qq": bot})
    monkeypatch.setattr(plugin, "config", Config())
    asyncio.run(plugin.send_weekly_post())
    bot.send_group_msg.assert_not_called()


def test_no_online_bots(monkeypatch):
    monkeypatch.setattr(plugin, "get_bots", lambda: {})
    monkeypatch.setattr(plugin, "config", Config(kfc_crazy_group_ids=[123]))
    asyncio.run(plugin.send_weekly_post())
