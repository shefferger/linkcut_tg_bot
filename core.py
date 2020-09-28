import telebot
import cfg  # cfg must include your bot TOKEN
import requests
import datetime

bot = telebot.TeleBot(cfg.TOKEN)


def log(info):
    print(info)
    with open('logs.txt', 'a') as logFile:
        logFile.write(info)


@bot.message_handler(content_types=['text'])
def main(msg):
    if msg.text == '/start':
        bot.send_message(msg.chat.id, 'Добро пожаловать в сокращатель ссылок! '
                                      'Просто введите ссылку и получите ее сокращенный вариант')
        return
    payload = {'link_in': msg.text}
    response = requests.post('http://www.linkcut.ru', data=payload)
    bot.send_message(msg.chat.id, response.text)
    logText = '\n' + str(datetime.datetime.now()) + ' UID: ' + msg.chat.id + ' Generated link: ' + response.text + '\n'
    log(logText)


log(str(datetime.datetime.now()) + 'Started Telegram Bot \'LinkCut.ru\'\n')
bot.polling(none_stop=True)
