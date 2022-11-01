import telebot
from config import *
from extensions import Converter, APIException
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = "Доброго времени суток! Вас приветствует помощник для конвертации валют.\n" \
           "Для получения дальнейших инструкций по работе помощника просим ввести команду: /helps.\n" \
           "Надеемся, что наш помощник будет Вам полезен!"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["helps"])
def helps(message: telebot.types.Message):
    text = "Напишите через пробел: \n- Валюту, цена которой Вас интересует.\n" \
           "- Валюту, в которой надо узнать цену первой валюты.\n" \
           "- Количество конвертируемой валюты.\n" \
           "Список доступных для конвертирования валют можно увидеть по команде: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = 'Доступные для конвертации валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException('Не удалось обработать указанное количество входных параметров.\n'
                               'Просим обратится за помощью к инструкции по команде /helps!')
        answer = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}. Просим обратится за помощью к инструкции по команде /helps!")
    else:
        bot.reply_to(message, answer)


bot.polling()
