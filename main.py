import telebot
from config import TOKEN, keys
from extensions import APIException, APIRequest


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_msg(message: telebot.types.Message):
    bot.reply_to(message, f'Добро пожаловать, {message.chat.username} 👋🏻\n'
                          f'Это бот для конвертации валют\n'
                          f'Формат ввода команды:\n'
                          f'<валюта, которую конвертируем> <валюта, в которую конвертируем> <количество первой валюты>\n'
                          f'Например, запрос "доллар рубль 10" - отобразит цену 10 долларов в рублях\n'
                          f'*Дробный разделитель "точка", округление при расчетах до 2 символов после точки\n'
                          f'Список доступных валют: /values')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    res = 'Доступны следующие валюты:\n'
    for key in keys.keys():
        res += f'{key}\n'
    bot.reply_to(message, f'{res}')


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        vls = message.text.split(' ')

        if len(vls) != 3:
            raise APIException('Некорректное количество параметров /help')

        base, quote, amount = vls
        total = APIRequest.get_price(base.lower(), quote.lower(), amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Возникла ошибка\n{e}')
    else:
        bot.reply_to(message, f'{amount} {base} = {total} {quote}')


bot.polling(none_stop=True)
