from wxpy import *

# 实例化，并登录微信

bot = Bot(cache_path=True)

# 调用图灵机器人API

tuling = Tuling(api_key='bb0bca2e5c0440b1855579de0486780e')

@bot.register()
def auto_reply(msg):
    tuling.do_reply(msg)

embed()