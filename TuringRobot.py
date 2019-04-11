from wxpy import *

bot = Bot(cache_path=True)

turing = Tuling(api_key='your_api_key')

print('叮叮叮, 机器人已经启动了！')

friend = bot.friends().search('')[0]

friend.send('如果你想和我聊天那么就开始吧')


@bot.register([Friend, TEXT])
def reply_my_friend(msg):
    turing.do_reply(msg)

embed()
