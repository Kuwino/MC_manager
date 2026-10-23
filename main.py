"""
Minecraft 服务器管理插件（AstrBot）

通过 RCON 远程管理简幻欢的 Minecraft 服务器。

命令：
    /list   查看在线玩家
    /say    向服务器广播一句话（/say 内容）
    /op     授予玩家 OP 权限（仅管理员，/op 玩家名）
    /stop   关闭服务器（仅管理员）

配置：
    在 AstrBot 面板「插件 → mc_manager → 配置」里填写 RCON 地址、端口和密码。
    密码不会硬编码在代码里，因此可以安全开源。
"""

from astrbot.api import AstrBotConfig
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent
from mcrcon import MCRcon


@register("mc_manager", "Kuwino", "Minecraft 服务器管理插件", "1.2.0")
class McManager(Star):
    """通过 RCON 管理 Minecraft 服务器。"""

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    def rcon(self, command: str) -> str:
        """执行一条 RCON 命令并返回结果。"""
        host = self.config.get("rcon_host", "play.simpfun.cn")
        port = self.config.get("rcon_port", 0)
        password = self.config.get("rcon_password", "")
        if not password:
            raise RuntimeError("未配置 RCON 密码，请在面板「插件 → mc_manager → 配置」里填写")
        if not port:
            raise RuntimeError("未配置 RCON 端口，请在面板「插件 → mc_manager → 配置」里填写")
        with MCRcon(host, password, port=int(port)) as mcr:
            return mcr.command(command)

    @filter.command("list")
    @filter.llm_tool(name="mc_list")
    async def cmd_list(self, event: AstrMessageEvent):
        """查看 Minecraft 服务器当前在线玩家和人数。

        Args:
        """
        try:
            yield event.plain_result("在线玩家：" + self.rcon("list"))
        except Exception as e:
            yield event.plain_result("查询失败：" + str(e))

    @filter.command("say")
    @filter.llm_tool(name="mc_say")
    async def cmd_say(self, event: AstrMessageEvent, content: str = ""):
        """向 Minecraft 服务器广播一句话。

        Args:
            content(string): 要广播的内容
        """
        if not content:
            parts = event.message_str.split(" ", 1)
            if len(parts) < 2:
                yield event.plain_result("用法：/say <内容>")
                return
            content = parts[1]
        try:
            self.rcon("say " + content)
            yield event.plain_result("已广播：" + content)
        except Exception as e:
            yield event.plain_result("广播失败：" + str(e))

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("op")
    async def cmd_op(self, event: AstrMessageEvent):
        """授予玩家 OP 权限：/op 玩家名（仅管理员）"""
        parts = event.message_str.split(" ", 1)
        if len(parts) < 2:
            yield event.plain_result("用法：/op <玩家名>")
            return
        try:
            self.rcon("op " + parts[1].strip())
            yield event.plain_result("已授权：" + parts[1].strip())
        except Exception as e:
            yield event.plain_result("操作失败：" + str(e))

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("stop")
    async def cmd_stop(self, event: AstrMessageEvent):
        """关闭服务器（仅管理员）"""
        try:
            self.rcon("stop")
            yield event.plain_result("已发送关服命令")
        except Exception as e:
            yield event.plain_result("关服失败：" + str(e))
