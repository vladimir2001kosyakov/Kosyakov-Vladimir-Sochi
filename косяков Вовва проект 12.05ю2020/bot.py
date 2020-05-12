from telegram.ext import Updater, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardRemove
import random
import requests

# Добавляем на клавиатуру кнопку вызывающую функцию randomword
reply_keyboard = [['/randomword']]


markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def start(update, context):
    update.message.reply_text(
        "Я бот. Предназначен для множества задач. Не общайтесь со мной ненормативным лексиконом."
        " /randomword - выводит случайное слово из словаря Ожегова со значением."
        " Если написать город в текстовом сообщении вы получите погоду."
        " Если бот не отвечает, проверьте правильность написания слова и повторите запрос.",
        reply_markup=markup
    )


def randomword(update, context):
    # Читаем словарь Ожегова построчно
    with open("words.txt") as inp:
        lines = inp.readlines()
    # Выбираем случайную строчку
    random_line = random.choice(lines).strip()
    update.message.reply_text(
        random_line,
    )


def weather(update, context):
    city = update.message.text
    # Проверяем введенный текст на нецензурную брань
    # f = open('ненормативный лексикон.txt')
    # if city.lower() in f.read().split(', '):
    #     update.message.reply_text('Мне обидно. Не общайтесь так со мной, пожалуйста.')
    # Формируем запрос на погоду в введенном городе
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/forecast?&units=metric&q=%s&appid=295f286d77a869327ed8dfae72a0542d' % (
            city))
    data = r.json()
    temp = data["list"]
    # Так как прогноз погоды выдается не мгновенный, подсчитываем среднюю температуру в ближайшее время.
    sr = (temp[0]["main"]["temp"] + temp[1]["main"]["temp"] + temp[2]["main"]["temp"]) / 3
    update.message.reply_text(
    'Средняя температура в ближайшее время ' + str(sr)[0:5] + '°C',
    )


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    REQUEST_KWARGS = {'proxy_url': 'socks5://127.0.0.1:9150'}
    updater = Updater('1111549264:AAEhdEQAFfiLngJCs5K4NjESX-GAKoTFEYE', use_context=True,
                      request_kwargs=REQUEST_KWARGS)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("randomword", randomword))
    dp.add_handler(CommandHandler("close", close_keyboard))
    text_handler = MessageHandler(Filters.text, weather)
    dp.add_handler(text_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
