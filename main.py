import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime

bot = telebot.TeleBot('6928695691:AAGu_Eu9Qj4gtHrrYIgtd1mLS5SFf-2Gm2o')


def make_appointment(message):
    bot.send_message(message.chat.id, "Введите ваше ФИО:")
    bot.register_next_step_handler(message, get_patient_fullname)


def get_patient_fullname(message):
    fullname = message.text
    bot.send_message(message.chat.id, "Выберите врача:", reply_markup=get_doctors_keyboard())
    bot.register_next_step_handler(message, lambda message: get_doctor(message, fullname))


def get_doctors_keyboard():
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(KeyboardButton('Хирург'))
    keyboard.add(KeyboardButton('Стоматолог'))
    keyboard.add(KeyboardButton('Терапевт'))
    keyboard.add(KeyboardButton(''))
    return keyboard


def get_doctor(message, fullname):
    doctor = message.text
    bot.send_message(message.chat.id, "Выберите дату и время:", reply_markup=get_time_keyboard())
    bot.register_next_step_handler(message, lambda message: confirm_appointment(message, fullname, doctor))


def get_time_keyboard():
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    for i in range(9, 18):
        time = datetime.strptime(str(i) + ':00', '%H:%M').time().strftime('%H:%M')
        keyboard.add(KeyboardButton(time))
    return keyboard


def confirm_appointment(message, fullname, doctor):
    time = message.text
    bot.send_message(message.chat.id, f"Вы записались к {doctor} на {time} на прием. Подтвердите запись.")


@bot.message_handler(commands=['start'])
def start(message):
    make_appointment(message)


bot.polling()