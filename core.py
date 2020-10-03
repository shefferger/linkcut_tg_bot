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
    try:
        response = requests.post('http://www.linkcut.ru', data=payload)
        text = response.text
    except requests.exceptions.ConnectionError:
        log.log('Connection Error')
        text = 'Временная ошибка сервера, попробуйте чуть позже'
    except requests.exceptions.BaseHTTPError:
        log.log('HTTP Error')
        text = 'Временная ошибка сервера, попробуйте чуть позже'
    bot.send_message(msg.chat.id, text)
    logText = '\tUID: ' + str(msg.chat.id) + '\tGenerated link: ' + text + '\n'
    log.log(logText)


log.log('Started LinkCut Telegram Bot')
bot.polling(none_stop=True)
