import telebot
from telebot import types
import requests
import re
import datetime


bot = telebot.TeleBot("", parse_mode=None)

regexpr = r"<tr class=\"ranking-list\">\n    <td class=\"rank ac\" valign=\"top\">\n    <span class=\"lightLink top-anime-rank-text rank3\">([0-9]+)</span>\n  </td>\n    <td class=\"title al va-t word-break\">\n    <a class=\"hoverinfo_trigger fl-l ml12 mr8\" href=\"(https://myanimelist.net/anime/[0-9]+/.*)\" id=\"#area[0-9]+\" rel=\"#info[0-9]+\">\n      <img width=\"50\" height=\"70\" alt=\"Anime: (.*)\" class=\"lazyload\" border=\"0\" data-src=\".*\" data-srcset=\".*\" />\n    </a>"
scoreregex = r"<td class=\"score ac fs14\"><div class=\"js-top-ranking-score-col di-ib al\"><i class=\"icon-score-star mr4 [on]+\"></i><span class=\"text on score-label score-[0-9A-Za-z]+\">(.*)</span></div>"
# [A-Z_!:.?\\\w/\-\s0-9qa-z]+
anime_saved = dict()
last_updated = dict()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    a = types.KeyboardButton('get 1-50')
    b = types.KeyboardButton('get 51-100')
    c = types.KeyboardButton('get 101-150')
    d = types.KeyboardButton('get 151-200')
    e = types.KeyboardButton('get 201-250')
    f = types.KeyboardButton('get 251-300')
    g = types.KeyboardButton('get 301-350')
    h = types.KeyboardButton('get 351-400')
    i = types.KeyboardButton('get 401-450')
    j = types.KeyboardButton("get 451-500")
    k = types.KeyboardButton("get 501-550")
    l = types.KeyboardButton("get 601-650")
    m = types.KeyboardButton("get 701-750")
    n = types.KeyboardButton("get 751-800")
    o = types.KeyboardButton("get 801-850")
    p = types.KeyboardButton("get 851-900")
    q = types.KeyboardButton("get 901-950")
    r = types.KeyboardButton("get 951-1000")
    markup.row(a, b, c, d, e, f, g, h, i)
    markup.row(j, k, l, m, n, o, p, q, r)
    bot.send_message(chat_id, "You can either select an existing option or type command get <n>.\nThis will show a list of anime ranked from n-th to (n + 49)-th places", reply_markup=markup)


@bot.message_handler(func=lambda m: ("hello" in m.text.lower() or 'привет' in m.text.lower()))
def echo_all(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, message.text)


@bot.message_handler(func=lambda x: 'get' in x.text)
def getlist(message):
    chat_id = message.chat.id
    user = message.from_user.username
    border = int(message.text.split()[-1].split('-')[0]) - 1
    file = open("log.txt", 'a')
    print(datetime.datetime.now(), user, border, file=file)
    print(datetime.datetime.now(), user, border)
    file.close()
    try:
        needed = False
        for i in range(border + 1, border + 51):
            if (datetime.datetime.now() - last_updated.get(i, datetime.datetime(1, 1, 1, 1, 1, 1))).total_seconds() > 60:
                needed = True
                break
        if needed:
            file = open("log.txt", "a")
            print("Didn't find in cache, trying to ask", file=file)
            print("Didn't find in cache, trying to ask")
            file.close()
            t = requests.get(f"https://myanimelist.net/topanime.php?limit={border}")

            scores = re.findall(scoreregex, t.content.decode())
            x = re.findall(regexpr, t.content.decode())
            y = re.findall(regexpr.replace("rank3", "rank2"), t.content.decode())
            z = re.findall(regexpr.replace("rank3", "rank1"), t.content.decode())
            v = re.findall(regexpr.replace("rank3", "rank4"), t.content.decode())
            u = re.findall(regexpr.replace("rank3", "rank5"), t.content.decode())
            x = z + y + x + v + u
            res = ''
            scores = scores
            for i in range(len(x)):
                score = (scores[i] if i < len(scores) else "N/A")
                res += x[i][0] + ': ' + x[i][2] + ' ' + ' (MAL Score: ' + score + ')\n'
                anime_saved[int(x[i][0])] = (x[i][2], x[i][1], score)
                last_updated[int(x[i][0])] = datetime.datetime.now()
            bot.send_message(chat_id, res)
        else:
            file = open("log.txt", "a")
            print("Found in cache", file=file)
            print("Found in cache")
            file.close()
            res = ''
            for i in range(border + 1, border + 51):
                res += str(i) + ": " + anime_saved[i][0] + ' ' + ' (MAL Score: ' + anime_saved[i][2] + ')\n'
            bot.send_message(chat_id, res)
    except:
        file = open("log.txt", 'a')
        print(datetime.datetime.now(), user, border, "DDOS", file=file)
        print(datetime.datetime.now(), user, border, "DDOS")
        file.close()
        bot.send_message(chat_id, "Sorry, it seems it a DDOS attack")


while True:
    try:
        bot.polling()
    except:
        pass
