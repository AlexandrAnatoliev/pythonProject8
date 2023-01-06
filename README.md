# pythonProject8

[Ru] БОТ, ДЛЯ TELEGRAM-КАНАЛА С РЕЦЕПТАМИ. По нажатию кнопки бот присылает случайный рецепт в личку сообщением.
Осуществляет поиск рецепта запросу пользователя "пирог с курицей" или "яйца колбаса майонез". Добавляет в текст рецепта рекламу

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

#### # Загружаем список рецептов из файла - рекламу аналогично

```python
f = open('recipes.txt', 'r', encoding='UTF-8')
recipes = f.read().split('\n')
f.close()
```

#### Если текстовый файл находится не в каталоге программы, то пишем полный путь к нему: "C:/Users/Александр/OneDrive/Рабочий стол/python/FreelanceTask2/freelanceTask3/firstText.txt" (использ.:'/'!)

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
    d_chars = {'А': 'A', 'а': 'a', 'В': 'B', 'е': 'e', 'Е': 'E', 'К': 'K', 'М': 'M', 'Н': 'H', 'о': 'o', 'О': 'O',
               'Р': 'P', 'с': 'c', 'С': 'C', 'Т': 'T', 'х': 'x', 'Х': 'X'}
    eng_question = []
    for word in ru_question:
        for char in d_chars:
            if char in word:
                while char in word:
                    word = word.replace(char, d_chars[char])
        eng_question.append(word[:-1])  # обрезаем окончание у слов "яблоки" -> "яблок"
    return eng_question, ru_question
```

#### Ищет совпадения слов из запроса пользователя в списке рецептов.
```python
start_index = 0  # с этого рецепта начинается поиск
 def search_recipe(question, recipes_list):
    question_index = len(question)  # Количество слов в запросе юзера
    answer = ''
    answer_count = 0
    global start_index

    for recipe in recipes_list[start_index:]:  # список от старта до конца
        counter = 0
        for word in question:
            recipe_low = str(recipe[:recipe.index("PEЦEПT:")].lower())  # берем только название рецепта и ингредиенты
            if word in recipe_low:
                counter += 1
        if answer_count < counter:  # если число совпадений слов больше предыдущего
            answer_count = counter
            answer = recipe  # принимаем рецепт как промежуточный ответ
        if answer_count == question_index:  # количество совпавших слов соответствует запросу
            start_index = recipes_list.index(recipe)
            return answer  # полное совпадение

    # если в одной половине списка нет, то искать в другой
    for recipe in recipes_list[:start_index]:  # список от начала до старта
        counter = 0
        for word in question:
            recipe_low = str(recipe.lower())
            if word in recipe_low:
                counter += 1
        if answer_count < counter:  # если число совпадений слов больше предыдущего
            answer_count = counter
            answer = recipe  # принимаем рецепт как промежуточный ответ
        if answer_count == question_index:  # количество совпавших слов соответствует запросу
            start_index = recipes_list.index(recipe)
            return answer  # полное совпадение
    return answer  # неполное совпадение запроса и ответа
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
        answer = random.choice(recipes)  # случайный рецепт
        answer += '\n\n' + promo
        # Отсылаем юзеру сообщение в его чат
        bot.send_message(message.chat.id, answer)
    elif len(user_question_en) > 1:  # если запрос содержит более одного слова
        answer = search_recipe(user_question_en, recipes)
        if len(answer) > 0:
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
