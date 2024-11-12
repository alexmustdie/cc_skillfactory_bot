import telebot

from config import TG_TOKEN
from extensions import *

api = API()
bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Format: {base}, {quote}, {amount}')

@bot.message_handler(commands=['values'])
def send_values(message):
    bot.send_message(message.chat.id, f'Values: {", ".join(api.get_values())}')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        base, quote, amount = message.text.split(' ')
        amount = float(amount)
        if base == quote:
            raise APIException('You gave me same values')
        if amount < 1:
            raise APIException('Amount must be greater than 1')
        if len([x for x in (base, quote) if x in api.get_values()]) != 2:
            raise APIException('I don\'t know such value')
        bot.send_message(message.chat.id, 'Wait...')
        price = api.get_price(base, quote, amount)
        bot.send_message(message.chat.id, '{:,.2f} {} is {:,.2f} {}'.format(amount, base, price, quote))
    except APIException as e:
        bot.send_message(message.chat.id, e)
    except Exception as e:
        bot.send_message(message.chat.id, 'Oops, there was some problem')
        print('{}: {}'.format(type(e).__name__, e))

if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        pass
