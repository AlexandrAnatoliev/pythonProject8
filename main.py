# pythonProject8

# БОТ, ДЛЯ TELEGRAM-КАНАЛА С РЕЦЕПТАМИ.
# По нажатию кнопки бот присылает случайный рецепт в личку.
# Осуществляет поиск рецепта запросу пользователя "пирог с курицей" или "яйца колбаса майонез".
# Добавляет в текст рецепта рекламу

import telebot
import random
from telebot import types

from config import token

try:
    # Загружаем список с рекламными объявлениями из файла promotions.txt
    try:  # этот блок не прерывает работу программы
        p = open('promotions.txt', 'r', encoding='UTF-8')
        prom_list = p.read().split('\n\n\n')
    finally:
        p.close()  # и закрывает открытый файл если он не прочитался

    # Загружаем список рецептов1
    try:
        f = open('recipes1.txt', 'r', encoding='UTF-8')
        recipes1 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов2
    try:
        f = open('recipes2.txt', 'r', encoding='UTF-8')
        recipes2 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов3
    try:
        f = open('recipes3.txt', 'r', encoding='UTF-8')
        recipes3 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов4
    try:
        f = open('recipes4.txt', 'r', encoding='UTF-8')
        recipes4 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов5
    try:
        f = open('recipes5.txt', 'r', encoding='UTF-8')
        recipes5 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов6
    try:
        f = open('recipes6.txt', 'r', encoding='UTF-8')
        recipes6 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов7
    try:
        f = open('recipes7.txt', 'r', encoding='UTF-8')
        recipes7 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов8
    try:
        f = open('recipes8.txt', 'r', encoding='UTF-8')
        recipes8 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов9
    try:
        f = open('recipes9.txt', 'r', encoding='UTF-8')
        recipes9 = f.read().split('\n\n\n')
    finally:
        f.close()

    # Загружаем список рецептов10
    try:
        f = open('recipes10.txt', 'r', encoding='UTF-8')
        recipes10 = f.read().split('\n\n\n')
    finally:
        f.close()

except FileNotFoundError:
    print("Невозможно открыть файл")
except:
    print("Ошибка при работе с файлами")


def random_recipe():
    """
    Выдает случайный список рецептов из заданных
    :return: список рецептов
    """
    lst_nomber = random.randint(1, 10)
    if lst_nomber == 1:
        print(1)  # todo убрать
        return recipes1
    elif lst_nomber == 2:
        print(2)
        return recipes2
    elif lst_nomber == 3:
        print(3)
        return recipes3
    elif lst_nomber == 4:
        print(4)
        return recipes4
    elif lst_nomber == 5:
        print(5)
        return recipes5
    elif lst_nomber == 6:
        print(6)
        return recipes6
    elif lst_nomber == 7:
        print(7)
        return recipes7
    elif lst_nomber == 8:
        print(8)
        return recipes8
    elif lst_nomber == 9:
        print(9)
        return recipes9
    else:
        print(10)
        return recipes10


# Создаем бота
bot = telebot.TeleBot(token)

start_index = 1  # с этого списка рецептов начинается поиск


def get_recept_list(start_ind=1):
    """
    По индексу файлы с рецептами
    :return: список рецептов
    """
    if start_ind == 1:
        return recipes1
    if start_ind == 2:
        return recipes2
    if start_ind == 3:
        return recipes3
    if start_ind == 4:
        return recipes4
    if start_ind == 5:
        return recipes5
    if start_ind == 6:
        return recipes6
    if start_ind == 7:
        return recipes7
    if start_ind == 8:
        return recipes8
    if start_ind == 9:
        return recipes9
    if start_ind == 10:
        return recipes10
    else:
        recipes1


def search_recipe(question):
    """
    Ищет совпадения слов из запроса пользователя в списке рецептов.
    :param question: Список слов запроса пользователя.
    :return: Искомый рецепт.
    """
    question_index = len(question)  # Количество слов в запросе юзера
    answer = ''
    answer_count = 0
    global start_index
    print(question)
    for index in range(start_index, 10+1):  # перебираем файлы от старта до конца
        print(index)
        for recipe in get_recept_list(index):  # список с рецептами от стартового списка до конца
            counter = 0
            for word in question:
                if "РЕЦЕПТ:" in recipe:  # если слово "РЕЦЕПТ" есть
                    recipe_low = str(
                        recipe[:recipe.index("РЕЦЕПТ:")].lower())  # берем только название рецепта и ингредиенты
                    if word in recipe_low:
                        counter += 1
            if answer_count < counter:  # если число совпадений слов больше предыдущего
                answer_count = counter
                answer = recipe  # принимаем рецепт как промежуточный ответ
            if answer_count == question_index:  # количество совпавших слов соответствует запросу
                start_index = index  # новый стартовый индекс
                return answer  # полное совпадение
    if start_index == 1:  # если поиск шел с самого начала
        return answer
    # если в одной половине списка нет, то искать в другой
    for index in range(1, start_index):
        for recipe in get_recept_list(index):  # список с рецептами от стартового списка до конца
            counter = 0
            for word in question:
                if "РЕЦЕПТ:" in recipe:  # если слово "РЕЦЕПТ" есть
                    recipe_low = str(
                        recipe[:recipe.index("РЕЦЕПТ:")].lower())  # берем только название рецепта и ингредиенты
                    if word in recipe_low:
                        counter += 1
            if answer_count < counter:  # если число совпадений слов больше предыдущего
                answer_count = counter
                answer = recipe  # принимаем рецепт как промежуточный ответ
            if answer_count == question_index:  # количество совпавших слов соответствует запросу
                start_index = index  # новый стартовый индекс
                return answer  # полное совпадение
    return answer  # выдаем что нашли


# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем кнопку
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Рецепт")
    markup.add(item1)
    bot.send_message(m.chat.id,
                     'Нажми: \n"Рецепт", чтобы получить случайный рецепт или "Пирог из яблок", если Вы ищете какое-то конкретное блюдо',
                     reply_markup=markup)


def get_question(question_in):
    """
    Формируем запрос юзера в виде ДВУХ списков (убираем предлоги "len(a) > 2"), уменьшаем регистр, заменяем часть букв на английские, обрезаем окончания у слов
    :param question_in: строка запроса от юзера
    :return: список слов для поиска [с заменой на английские буквы], [только русские буквы]
    """
    ru_question = [a.lower() for a in question_in.text.split() if len(a) > 2]
    # словарь 'русская буква':'латинская буква'
    d_chars = {'а': 'a', 'е': 'e', 'о': 'o', 'с': 'c', 'х': 'x'}

    eng_question = []
    for word in ru_question:
        for char in d_chars:
            if char == word[0]:  # если первая буква в рецепте была заглавная, то она может быть и русской!!!
                first_char = char  # первая буква
                word2 = word[1:]  # остальная часть слова
                for char in d_chars:
                    if char in word2:
                        while char in word2:
                            word2 = word2.replace(char, d_chars[char])
                word2 = first_char + word2
                eng_question.append(word2[:-1])  # добавляем аналог слова с первой русской буквой
            if char in word:
                while char in word:
                    word = word.replace(char, d_chars[char])
        word = word.lower()  # уменьшаем регистр, чтобы не зависеть от него в поиске
        eng_question.append(word[:-1])  # обрезаем окончание у слов "яблоки" -> "яблок"
    return eng_question, ru_question


# Получает сообщение от юзера и формирует ему ответ
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Формируем запрос юзера в виде списка (убираем предлоги) и уменьшаем регистр [английские буквы], [русские]
    user_question_en, user_question_ru = get_question(message)
    promo = random.choice(prom_list)  # реклама

    # Если сообщение от юзера содержит слово "рецепт" (!рецепт содержит английские буквы), выдает ему случайный рецепт
    if 'рецепт' in user_question_ru:  # правильные запросы "Рецепт" и "рецепт"
        recipes = random_recipe()  # выбираем случайный список рецептов
        answer = random.choice(recipes)  # случайный рецепт
        if len(answer) > 10:  # если текст рецепта достаточной длины todo добавить везде
            answer += '\n\n' + promo
        else:
            answer = random.choice(recipes)  # еще раз
            answer += '\n\n' + promo
        # Отсылаем юзеру сообщение в его чат
        bot.send_message(message.chat.id, answer)
    elif len(user_question_en) > 1:  # если запрос содержит более одного слова
        answer = search_recipe(user_question_en)
        if answer is not None:
            answer += '\n\n' + promo
            # посылаем юзеру найденный рецепт
            bot.send_message(message.chat.id, answer)
        else:
            bot.send_message(message.chat.id, """К сожалению, я не знаю таких слов. Напишите мне:
                         \n \"Рецепт\", чтобы получить случайный рецепт.
                         \n "Пирог из яблок", если Вы ищете какое-то конкретное блюдо
                         \n "Яйца яблоки бананы", в случае, если нужен совет, что приготовить из конкретных продуктов""")
    else:
        bot.send_message(message.chat.id,
                         "К сожалению, слишком короткий запрос. Напишите подробней: \"Пирог из яблок\"")


# Запускаем бота
bot.polling(none_stop=True, interval=0)
