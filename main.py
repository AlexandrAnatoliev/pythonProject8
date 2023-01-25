# pythonProject8

# БОТ, ДЛЯ TELEGRAM-чата С РЕЦЕПТАМИ.
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
except FileNotFoundError:
    print("Невозможно открыть файл promotions.txt")
except:
    print("Ошибка при работе с файлом promotions.txt")

try:
    # список с путями к рецептам
    path_list = ['rec1/recipes1.txt', 'rec1/recipes2.txt', 'rec1/recipes3.txt', 'rec1/recipes4.txt',
                 'rec1/recipes5.txt', 'rec1/recipes6.txt', 'rec1/recipes7.txt', 'rec1/recipes8.txt',
                 'rec1/recipes9.txt', 'rec1/recipes10.txt', 'rec2/recipes11.txt', 'rec2/recipes12.txt',
                 'rec2/recipes13.txt', 'rec2/recipes14.txt', 'rec2/recipes15.txt', 'rec2/recipes16.txt',
                 'rec2/recipes17.txt', 'rec2/recipes18.txt', 'rec2/recipes19.txt', 'rec2/recipes20.txt',
                 'rec3/recipes21.txt', 'rec3/recipes22.txt', 'rec3/recipes23.txt', 'rec3/recipes24.txt',
                 'rec3/recipes25.txt', 'rec3/recipes26.txt', 'rec3/recipes27.txt', 'rec3/recipes28.txt',
                 'rec3/recipes29.txt', 'rec3/recipes30.txt', 'rec4/recipes31.txt', 'rec4/recipes32.txt',
                 'rec4/recipes33.txt', 'rec4/recipes34.txt',
                 'rec4/recipes35.txt', 'rec4/recipes36.txt', 'rec4/recipes37.txt', 'rec4/recipes38.txt',
                 'rec4/recipes39.txt', 'rec4/recipes40.txt', 'rec4/recipes41.txt', 'rec4/recipes42.txt',
                 'rec5/recipes43.txt', 'rec5/recipes44.txt', 'rec5/recipes45.txt', 'rec5/recipes46.txt',
                 'rec5/recipes47.txt', 'rec5/recipes48.txt', 'rec5/recipes49.txt', 'rec5/recipes50.txt',
                 'rec5/recipes51.txt', 'rec5/recipes52.txt', 'rec5/recipes53.txt', 'rec5/recipes54.txt']
    r_list = []  # Список списков с рецептами

    # Загружаем список рецептов1
    for path_recipes in path_list:
        try:
            f = open(path_recipes, 'r', encoding='UTF-8')
            r_list.append(f.read().split('\n\n\n'))
        finally:
            f.close()
except FileNotFoundError:
    print(f"Невозможно открыть файл: {path_list[len(r_list)]}")
except:
    print(f"Ошибка при работе с файлами {path_list[len(r_list)]}")

print(f"загружено {len(r_list)} файлов")
# Создаем бота
bot = telebot.TeleBot(token)

start_index = 0  # с этого рецепта начинается поиск


def get_recept_list(start_ind=0):
    """
    По индексу файла с рецептами
    :return: возвращает список рецептов
    """
    return r_list[start_ind]


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

    # print(start_index)  # проверка работоспособности - выводит номер списка с рецептами

    for index in range(start_index, len(r_list)):  # перебираем файлы от старта до конца

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
    if start_index == 0:  # если поиск шел с самого начала
        return answer
    # если в одной половине списка нет, то искать в другой
    for index in range(0, start_index):
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
        recipes = random.choice(r_list)  # выбираем случайный список рецептов из списка рецептов

        # print(r_list.index(recipes))  # выводит номер списка с рецептами для проверки

        answer = random.choice(recipes)  # случайный рецепт
        if len(answer) > 10:  # если текст рецепта достаточной длины
            answer += '\n\n' + promo
        else:
            answer = random.choice(recipes)  # еще раз
            answer += '\n\n' + promo
        # Отсылаем юзеру сообщение в его чат
        bot.send_message(message.chat.id, answer)
    elif len(user_question_en) > 1:  # если запрос содержит более одного слова
        answer = search_recipe(user_question_en)
        if len(answer) > 10:
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
