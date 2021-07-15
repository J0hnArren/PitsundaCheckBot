from telebot import *

with open(".env", "r") as f:
    TOKEN = f.read()

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, send me a pic with dog or cat")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


def main():
    # bot.polling()
    bot.infinity_polling()


if __name__ == '__main__':
    main()
