# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from wxpy import *

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]


# 初始化机器人
chatbot = ChatBot("Ron Obvious")
trainer = ListTrainer(chatbot)
trainer.train(conversation)
# trainer.set_trainer(ChatterBotCorpusTrainer)

# 这里先使用该库现成的中文语料库训练
trainer.train("chatterbot.corpus.chinese")

# 这里进行简单测试
print(chatbot.get_response("很高兴认识你"))

# 也可以自定义训练
# 比如当前输入”讲个笑话“
print(chatbot.get_response('讲个笑话'))

# 使用ListTrainer进行自定义训练，输入内容为一个列表
# trainer.set_trainer(ListTrainer)
trainer.train([
    "讲个笑话",
    "一天和同学出去吃饭，买单的时候想跟服务员开下玩笑。“哎呀，今天没带钱出来埃”“你可以刷卡。”“可是我也没带卡出来的埃”“那你可以刷碗“",
])

print(chatbot.get_response("讲个笑话"))

# 初始化机器人，这里会生成一张二维码，用微信扫码继续登陆
bot = Bot()
print(bot)
# 获取好友列表，这里随意使用一个好友进行测试
bot.friends()
print(bot.friends())
friend = bot.friends()[2]
print(friend)
# 向好友发送消息
friend.send('hi')
# 使用机器人进行自动回复
@bot.register(friend)
def reply_my_friend(msg):
    return chatbot.get_response(msg.text).text