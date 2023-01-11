# pythonProject8

[Ru] БОТ, ДЛЯ TELEGRAM-КАНАЛА С РЕЦЕПТАМИ. По нажатию кнопки бот присылает случайный рецепт в личку сообщением.
Осуществляет поиск рецепта запросу пользователя "пирог с курицей" или "яйца колбаса майонез". Добавляет в текст рецепта
рекламу

## Требования

* $ pip install -r требования.txt
* создать файл promotions.txt, содержащий список с рекламных объявлений
* создать файл recipes.txt, который содержит список рецептов. ВАЖНО! На каждой строке файлов находится по одному
  анекдоту
* создать файл config.py, в котором будут храниться токен для доступа к боту и адрес канала в виде

```python
token = "1234567890:ASDFGHH..."
channel = '@topjokes...'
```

## Где взять токен?

* https://xakep.ru/2021/11/28/python-telegram-bots/

## Подключаем модули

```python
import telebot
import random
from telebot import types
from config import token
```

## Примеры использования

#### Обработка исключений

#### Если текстовый файл находится не в каталоге программы, то пишем полный путь к нему: "C:/Users/Александр/OneDrive/Рабочий стол/python/FreelanceTask2/freelanceTask3/firstText.txt" (использ.:'/'!)

Закрывает открытый файл, если он не прочитался

```python
# Загружаем список с рекламными объявлениями из файла promotions.txt
try:  # этот блок не прерывает работу программы 
    p = open('promotions.txt', 'r', encoding='UTF-8')
    prom_list = p.read().split('\n\n\n')
finally:
    p.close()  # и закрывает открытый файл если он не прочитался
```

Этот блок прерывает работу программы и пишет причину

```python
try:
except FileNotFoundError:
    print("Невозможно открыть файл")
except:
    print("Ошибка при работе с файлами")
```

#### Выдает случайный список рецептов из заданных

```python
def random_recipe():
    lst_nomber = random.randint(1, 10)
    if lst_nomber == 1:
        return recipes1
    elif lst_nomber == 2:
        return recipes2
    else:
        return recipes10
```

#### При поиске рецепта перебирает индекс

```python
start_index = 1  # с этого списка рецептов начинается поиск


def search_recipe(question):
    global start_index
    for index in range(start_index, 10 + 1):
```

#### и по индексу возвращает файл с рецептами

```python
def get_recept_list(start_ind=1):
    if start_ind == 1:
        return recipes1
    if start_ind == 10:
        return recipes10
    else:
        recipes1
```

#### Добавляем кнопку

```python
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
```

#### Формируем запрос юзера в виде двух списков - с английскими и русским буквами (убираем предлоги "len(a) > 2"), уменьшаем регистр, заменяем часть букв на английские, обрезаем окончания у слов

```python
def get_question(question_in):
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
```

#### Ищет совпадения слов из запроса пользователя в списке рецептов.

```python
start_index = 1  # с этого рецепта начинается поиск

def search_recipe(question):
    question_index = len(question)  # Количество слов в запросе юзера
    answer = ''
    answer_count = 0
    global start_index

    for index in range(start_index, 10 + 1):  # перебираем файлы от старта до конца

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
```

#### Получает сообщение от юзера и формирует ему ответ

```python
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Формируем запрос юзера в виде списка (убираем предлоги) и уменьшаем регистр [английские буквы], [русские]
    user_question_en, user_question_ru = get_question(message)
    promo = random.choice(prom_list)  # реклама

    # Если сообщение от юзера содержит слово "рецепт" (!рецепт содержит английские буквы), выдает ему случайный рецепт
    if 'рецепт' in user_question_ru:  # правильные запросы "Рецепт" и "рецепт"
        recipes = random_recipe()  # выбираем случайный список рецептов
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
```

#### Запускаем бота

```python
bot.polling(none_stop=True, interval=0)
```
