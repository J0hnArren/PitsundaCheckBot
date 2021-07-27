from telebot import *
from image_prediction import Dogs_vs_Cats
import os
from requests.exceptions import ConnectTimeout

with open(".env", "r") as f:
    TOKEN = f.read()

bot = TeleBot(TOKEN)
model = Dogs_vs_Cats("package/", 224)


def keyboard():
    btn1 = '/start'
    btn23 = ['FAQ', '/help']
    keyboard_markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
    keyboard_markup.add(btn1)
    keyboard_markup.add(*btn23)
    return keyboard_markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    # username
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}! "
                                      "Send me a photo with a cat or a dog and I will guess who is in the photo.",
                     reply_markup=keyboard())

    Dogs_vs_Cats.clear_data()


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Send me a pic with dog or cat")


@bot.message_handler(content_types=["text"])
def show_info(message):
    try:
        if message.text == 'FAQ':
            bot.send_message(message.chat.id, "1. The bot recognized the image incorrectly, why? "
                                              "The recognition accuracy is almost 99%. The reasons for the error may be as follows:\n"
                                              "- The photo is very blurry or fuzzy\n"
                                              "- The photo shows a drawing or screenshot from a cartoon with a cat or dog\n"
                                              "- The photo shows both a cat and a dog, or there are neither of them at all "
                                              "(the neural network is not designed to recognize other objects)\n"
                                              "2. Why is the bot called Pitsunda? Because she's a cute kitty! Isn't she?")
            bot.send_photo(message.chat.id, "https://i.imgur.com/EiRZ7fr.jpeg")
        else:
            bot.reply_to(message, "LOL " + message.text)
    except ConnectTimeout as e:
        print(e)
        bot.reply_to(message, "Something went wrong with connection. Try again")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Something went wrong. Try again")


@bot.message_handler(content_types=['photo'])
def handle_picture(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        _, file_extension = os.path.splitext(file_info.file_path)
        filename = message.photo[1].file_id + file_extension

        src = 'data/'
        with open(src + filename, 'wb') as new_file:
            new_file.write(downloaded_file)

        if make_prediction(src, filename):
            bot.reply_to(message, "This is a dog")
        else:
            bot.reply_to(message, "This is a cat")

    except ConnectTimeout as e:
        print(e)
        bot.reply_to(message, "Something went wrong with connection. Try again")
    except Exception as e:
        print(e)
        bot.reply_to(message, "Something went wrong. Resend the image, please.")


def make_prediction(src, filename):
    return model.predict(src, filename)


def main():
    # bot.polling()
    bot.infinity_polling()


if __name__ == '__main__':
    main()
