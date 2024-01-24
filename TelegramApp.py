import telebot
from config import currency, TOKEN
from extensions import ConvertionException, CryptoConverter
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start_help_message(message: telebot.types.Message):
    text = ('Чтобы конвертировать валюту, напишите сообщение боту в такой форме\n <имя валюты> \n<в какую перевести> \n<количество валюты> \
    Список доступных валют: /values \n ПРОЕКТ НАХОДИТСЯ В РАЗРАБОТКЕ!')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value_message(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException(f'Слишком много параметров.')
        elif len(values) < 3:
            raise ConvertionException(f'Слишком мало параметров')
        else:
            quote, base, amount = values
            total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()