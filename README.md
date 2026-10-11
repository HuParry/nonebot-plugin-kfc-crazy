<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-kfc-crazy

_✨ 🍗 疯狂星期四 🍗 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-kfc-crazy.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-kfc-crazy">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-kfc-crazy.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

## 📖 介绍

一个适用于 NoneBot2 和 OneBot V11 QQ 机器人的疯狂星期四语录插件。

- 在群聊或私聊中发送完整消息 `疯狂星期四`，机器人随机回复一条语录，无需命令前缀或 @。
- 每周星期四上午 **10:00（北京时间，Asia/Shanghai）**，机器人向配置的 QQ 群自动发送随机语录。
- 两种发送方式均从 `nonebot_plugin_kfc_crazy/post.json` 的 `post` 数组中随机选取语录，并沿用相同的文本处理逻辑。

## 💿 安装

定时功能依赖 [nonebot-plugin-apscheduler](https://github.com/nonebot/plugin-apscheduler)。通过下列方式安装本插件时会一并安装该依赖，插件加载时也会自动加载 APScheduler，无需重复添加。

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-kfc-crazy

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目根目录下打开命令行，使用运行机器人的 Python 环境，根据你使用的包管理器执行相应的安装命令：

<details>
<summary>pip</summary>

    pip install nonebot-plugin-kfc-crazy
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-kfc-crazy
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-kfc-crazy
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-kfc-crazy
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_template"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

```dotenv
KFC_CRAZY_GROUP_IDS=[123456789,987654321]
```

|        配置项         | 必填 | 默认值 |                     说明                     |
|:---------------------:|:----:|:------:|:--------------------------------------------:|
| `kfc_crazy_group_ids` |  否  |  `[]`  | 定时发送的 QQ 群号集合，重复群号会自动去重。 |

不配置或设置为 `[]` 时，不发送定时群消息，修改配置后需重启机器人。

定时任务固定使用北京时间，每周四上午 10:00 执行。

## 🎉 使用

### 指令表

|     指令     |  权限  | 需要@ |    范围    |                      说明                      |
|:------------:|:------:|:-----:|:----------:|:----------------------------------------------:|
| `疯狂星期四` | 所有人 |  否   | 群聊、私聊 | 随机回复一条疯狂星期四语录，手动触发不限星期。 |

直接发送完整消息 `疯狂星期四` 即可，无需 `/` 等命令前缀。其他星期或日文触发词不属于本插件的指令。

配置目标群后，每周四上午 10:00 会自动发送语录，不需要群成员发送指令。

### 效果图
