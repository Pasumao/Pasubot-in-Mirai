import nonebot
from nonebot.adapters.mirai import WebsocketBot


nonebot.init()
nonebot.get_driver().register_adapter('mirai-ws', WebsocketBot, qq=764574914)
nonebot.load_builtin_plugins()
nonebot.load_plugins("awesome_bot/plugins")
app = nonebot.get_asgi()

if __name__ == "__main__":
    nonebot.run()
