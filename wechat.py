from wxpy import *
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as fm
from wordcloud import WordCloud, ImageColorGenerator
from os import path
import jieba
bot = Bot(cache_path=True)
mpl.rcParams['font.sans-serif'] = ['SimHei']
d = path.dirname(__file__)
stopwords_path = d + '/static/stopwords.txt'


def plt_city_paint():
    n_groups = 10
    city_weight = (25.5, 16.0, 2.5, 2.0, 1.5, 1.5, 1.0, 1.0, 1.0, 1.0)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, city_weight, bar_width, alpha=opacity, color='b', error_kw=error_config, label='城市')
    ax.set_xlabel('城市名称')
    ax.set_ylabel('数据占比(%)')
    ax.set_title('好友城市Top10')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('潍坊', '青岛', '海淀', '日照', '枣庄', '烟台', 'Darwin', '泰安', '济宁', '临沂'))
    # 天知道为什么我有一个达尔文地区的好友
    ax.legend()
    fig.tight_layout()
    plt.show()


def plt_province_paint():
    n_groups = 10
    city_weight = (54.0, 3.0, 1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, city_weight, bar_width, alpha=opacity, color='b', error_kw=error_config, label='省份')
    ax.set_xlabel('省份名称')
    ax.set_ylabel('数据占比(%)')
    ax.set_title('好友省份Top10')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('山东', '北京', '广东', 'Northern Territory', '安徽', 'Dubayy', '浙江', '江西', '江苏', '天津'))
    # 天知道为什么我有Northern Territory， Dubayy？？？？ (这又是哪里)地区的好友
    ax.legend()
    fig.tight_layout()
    plt.show()


def print_friend_stats_text():
    my_friends = bot.friends(update=False)
    print(my_friends.stats_text())


def sex_pie_paint():
    labels = ['男性', '女性', '其他']
    sizes = [53.0, 35.0, 12.0]
    explode = (0, 0.1, 0)
    # 如果我有女朋友的话 我估计不敢让她知道我自己有这么多的女性好友 哈哈哈
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    # 纵横相等，画成一个圆
    ax1.axis('equal')
    plt.legend()
    plt.show()


def jieba_clear_text(text_j):
    my_word_list = []
    seg_list = jieba.cut(text_j, cut_all=False)
    list_str = '/.'.join(seg_list)
    list_str = list_str.replace("class", "")
    list_str = list_str.replace("span", "")
    list_str = list_str.replace("emoji", "")

    # 打开停用词表
    f_stop = open(stopwords_path, encoding="utf8")
    # 读取
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()  # 关闭资源

    f_stop_seg_list = f_stop_text.split('\n')
    for my_word in list_str.split('/'):
        if not(my_word.split()) in f_stop_seg_list and len(my_word.strip()) > 1:
            my_word_list.append(my_word)

    return ' '.join(my_word_list)


def make_word_cloud(text_1, i):
    background = plt.imread('back.png')
    word_cloud = WordCloud(
        background_color='#FFFFFF',
        width=990,
        height=440,
        mask=background,
        margin=10,
        max_font_size=70,
        random_state=20,
        font_path='/static/simkai.ttf'
    ).generate(text_1)
    my_font = fm.FontProperties(fname=d+'/static/simkai.ttf')
    bg_color = ImageColorGenerator(background)
    plt.imshow(word_cloud.recolor(color_func=bg_color))
    plt.axis('off')
    word_cloud.to_file(d+r"/image/render_0%d.png" % i)
    plt.show()


def nick_name_and_signature():
    my_friends = bot.friends()
    nick_name = ''
    wx_signature = ''
    for friend in my_friends:
        nick_name = nick_name + friend.raw['NickName']
        wx_signature = wx_signature + friend.raw['Signature']

    nick_name = jieba_clear_text(nick_name)
    wx_signature = jieba_clear_text(wx_signature)
    make_word_cloud(nick_name, 1)
    make_word_cloud(wx_signature, 2)


@bot.register(msg_types=FRIENDS)
# 自动接受验证信息中包含 ‘我是’ 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if '我是' in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        new_friend.send('哈哈，我自动接受了你的好友请求')


def print_friends_mps_groups_list():
    print(bot.friends(), bot.mps(), bot.groups())


# class_group = ensure_one(bot.groups().search('Python进阶选修课'))
# teacher = ensure_one(class_group.search('刘晓洁'))
class_group = ensure_one(bot.groups().search('③不正经交流群【禁推】'))
teacher = ensure_one(class_group.search('蓝色的海'))
# 在群里就是这个名字


@bot.register(class_group)
def forward_teacher_msg(msg):
    if msg.member == teacher:
        msg.forward(bot.file_helper, prefix='老师发言:')


# embed()


# 反正用的时候两个选一个吧 我也不知道为什么  可能是我的操作原因导致的两个不能同时起作用
@bot.register()
def print_msg(msg):
    print(msg)

# embed()


@bot.register([Friend, Group], TEXT)
def auto_reply(msg):
    if isinstance(msg.chat, Group) and not msg.is_at:
        return
    else:
        return '收到消息: {} ({})'.format(msg.text, msg.type)


print_friend_stats_text()
