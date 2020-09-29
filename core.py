import telebot
import cfg  # cfg must include your bot TOKEN
import requests
import s_logger as log

bot = telebot.TeleBot(cfg.TOKEN)


@bot.message_handler(content_types=['text'])
def main(msg):
    if msg.text == '/start':
        bot.send_message(msg.chat.id, 'Добро пожаловать в сокращатель ссылок! '
                                      'Просто введите ссылку и получите ее сокращенный вариант')
        return
    payload = {'link_in': msg.text, 'userType': 'telegramBot'}
    response = requests.post('http://www.linkcut.ru', data=payload)
    if response.status_code in (500, 404, 400):
        return
    bot.send_message(msg.chat.id, response.text)
    logText = ' UID: ' + str(msg.chat.id) + ' Generated link: ' + response.text
    log.log(logText)


log.log('Started LinkCut Telegram Bot')
bot.polling(none_stop=True)
