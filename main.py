# pythonProject8

# БОТ, ДЛЯ TELEGRAM-КАНАЛА С РЕЦЕПТАМИ
# По нажатию кнопки бот присылает случайный рецепт в личку

import telebot
import random
from telebot import types

from config import token

# Загружаем список анекдотов из файла
# если текстовый файл находится не в каталоге программы, то пишем полный путь к нему
# "C:/Users/Александр/OneDrive/Рабочий стол/python/FreelanceTask2/freelanceTask3/firstText.txt" (использ.:'/'!)
f = open('recipes.txt', 'r', encoding='UTF-8')
recipes = f.read().split('\n\n\n')
f.close()

# Создаем бота
bot = telebot.TeleBot(token)


# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем кнопку
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рецепт")
    markup.add(item1)
    bot.send_message(m.chat.id,
                     'Нажми: \nРецепт для получения свежего рецепта ',
                     reply_markup=markup)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Формируем запрос юзера в виде списка (убираем предлоги) и уменьшаем регистр
    user_question = [a.lower() for a in message.text.split() if len(a) > 3]

    # Если юзер прислал "Рецепт", выдаем ему случайный рецепт
    if 'рецепт' in user_question:  # правильные запросы "Рецепт" и "рецепт"
        answer = random.choice(recipes)
        # Отсылаем юзеру сообщение в его чат
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, "К сожалению, я не знаю таких слов. Напишите мне: \"Рецепт\"")


# Запускаем бота
bot.polling(none_stop=True, interval=0)
