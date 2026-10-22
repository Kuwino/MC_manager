# MC 服务器管理（AstrBot 插件）

通过 RCON 远程管理 Minecraft 服务器的 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 插件，适用于[简幻欢](https://www.simpfun.cn/)等面板服。

## 功能

| 命令 | 说明 | 权限 |
| --- | --- | --- |
| `/list` | 查看在线玩家 | 所有人 |
| `/say <内容>` | 向服务器广播一句话 | 所有人 |
| `/op <玩家名>` | 授予玩家 OP 权限 | 仅管理员 |
| `/stop` | 关闭服务器 | 仅管理员 |

## 安装

### 方式一：从插件市场安装

在 AstrBot 管理面板「插件市场」中搜索 `mc_manager` 安装。

### 方式二：手动安装

把本仓库 clone 到 AstrBot 的插件目录：

```bash
cd /opt/astrbot/data/plugins
git clone <仓库地址> mc_manager
```

安装依赖（mcrcon）：

```bash
/opt/astrbot/venv/bin/pip install mcrcon
```

然后在 WebUI「插件」页找到本插件，点「重载」。

## 配置

在 WebUI「插件 → MC 服务器管理 → 配置」里填写：

| 配置项 | 说明 | 默认值 |
| --- | --- | --- |
| RCON 服务器地址 | 简幻欢直连入口域名 | `play.simpfun.cn` |
| RCON 端口 | 简幻欢「实例端口」页分配的端口 | `19166` |
| RCON 密码 | `server.properties` 里的 `rcon.password` | 空（必填） |

> RCON 密码不硬编码在代码里，而是在面板里填写（以密码框遮罩显示），因此可以安全开源。

## 管理员配置

`/op` 和 `/stop` 需要管理员权限。在 QQ 里对机器人发 `/sid` 获取你的用户 ID，然后到 AstrBot 面板「配置文件 → 管理员 ID」里填写。

## 依赖

- [mcrcon](https://github.com/RedNoodleMinecraft/mcrcon)

## 许可证

[MIT](LICENSE)
