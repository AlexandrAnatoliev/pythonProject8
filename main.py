# pythonProject8

# БОТ, ДЛЯ TELEGRAM-КАНАЛА С РЕЦЕПТАМИ
# По нажатию кнопки бот присылает случайный рецепт в личку

import telebot
import random
from telebot import types

from config import token

# Загружаем список рецептов из файла recipes.txt
# если текстовый файл находится не в каталоге программы, то пишем полный путь к нему
# "C:/Users/Александр/OneDrive/Рабочий стол/python/FreelanceTask2/freelanceTask3/firstText.txt" (использ.:'/'!)
f = open('recipes.txt', 'r', encoding='UTF-8')
recipes = f.read().split('\n\n\n')
f.close()

# Загружаем список с рекламными объявлениями из файла promotions.txt
p = open('promotions.txt', 'r', encoding='UTF-8')
prom_list = p.read().split('\n\n\n')
p.close()

# Создаем бота
bot = telebot.TeleBot(token)


def search_recipe(question, recipes_list):
    """
    Ищет совпадения слов из запроса пользователя в списке рецептов.
    :param recipes_list: Список рецептов.
    :param question: Список слов запроса пользователя.
    :return: Искомый рецепт.
    """
    question_index = len(question)  # Количество слов в запросе юзера
    answer = ''
    answer_count = 0
    for recipe in recipes_list:
        counter = 0
        for word in question:
            word = str(word[:-1])
            recipe_low = str(recipe.lower())
            if word in recipe_low:
                counter += 1
        if answer_count < counter:  # если число совпадений слов больше предыдущего
            answer_count = counter
            answer = recipe  # принимаем рецепт как промежуточный ответ
        if answer_count == question_index:  # количество совпавших слов соответствует запросу
            return answer  # полное совпадение
    return answer  # неполное совпадение запроса и ответа


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
    # словарь 'русская буква':'латинская буква'
    d_chars = {'А': 'A', 'а': 'a', 'В': 'B', 'е': 'e', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'о': 'o', 'О': 'O',
               'Р': 'P', 'с': 'c', 'С': 'C', 'Т': 'T', 'х': 'x', 'Х': 'X'}
    # заменяем русские буквы на английские
    user_question2 = []
    for word in user_question:
        for char in d_chars:
            if char in word:
                while char in word:
                    word = word.replace(char, d_chars[char])
        user_question2.append(word)

    promo = random.choice(prom_list)  # реклама

    # Если сообщение от юзера содержит слово "рецепт", выдает ему случайный рецепт
    if 'рецепт' in user_question and len(user_question) == 1:  # правильные запросы "Рецепт" и "рецепт"
        answer = random.choice(recipes)  # рецепт
        answer += '\n\n' + promo
        # Отсылаем юзеру сообщение в его чат
        bot.send_message(message.chat.id, answer)
    elif len(user_question) > 1:
        answer = search_recipe(user_question2, recipes)
        if len(answer) > 0:
            answer += '\n\n' + promo
            # посылаем юзеру найденный рецепт
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, "К сожалению, я не нашел такого рецепта. Напишите мне: \"Рецепт\"")
    else:
        bot.send_message(message.chat.id, "К сожалению, я не знаю таких слов. Напишите мне: \"Рецепт\"")


# Запускаем бота
bot.polling(none_stop=True, interval=0)
