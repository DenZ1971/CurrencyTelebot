import telebot
from config import TOKEN, keys
from utils import ConvercionExeption, ValueConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите коменду боту в следующем формате:\n<название валюты>\
<в какую валюту перевести><сумму пепеводимой валюты>\nСписок доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands =['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise ConvercionExeption('Слишком много параметров')

        quote, base, amount = values

        total_base = ValueConverter.convert(quote, base, amount)
    except ConvercionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} = {float(total_base) * float(amount)}'
        bot.send_message(message.chat.id, text)




bot.polling(none_stop = True)


