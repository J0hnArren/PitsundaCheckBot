from telebot import *
from image_prediction import Dogs_vs_Cats
import os

with open(".env", "r") as f:
    TOKEN = f.read()

bot = TeleBot(TOKEN)
model = Dogs_vs_Cats("package/", 224)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello, send me a pic with dog or cat")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


@bot.message_handler(content_types=['photo'])
def handle_picture(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    _, file_extension = os.path.splitext(file_info.file_path)
    filename = message.photo[1].file_id

    src = 'data/'
    with open(src + filename + file_extension, 'wb') as new_file:
        new_file.write(downloaded_file)

    if make_prediction(src):
        bot.reply_to(message, "This is a dog")
    else:
        bot.reply_to(message, "This is a cat")


# @bot.message_handler(content_types=["text"])
# def repeat_all_messages(message):
#     bot.send_message(message.chat.id, message.text)

def make_prediction(src):
    return model.predict(src)


def main():
    # bot.polling()
    bot.infinity_polling()


if __name__ == '__main__':
    main()
