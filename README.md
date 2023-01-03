# pythonProject3

[Ru] БОТ, ДЛЯ TELEGRAM-КАНАЛА С АНЕКДОТАМИ. По нажатию кнопки бот присылает случайный анекдот в личку сообщение.

## Требования

* $ pip install -r требования.txt
* создать файл funs.txt, который содержит список анекдотов. ВАЖНО! На каждой строке файлов находится по одному анекдоту
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

#### # Загружаем список анекдотов из файла

```python
f = open('recipes.txt', 'r', encoding='UTF-8')
funs = f.read().split('\n')
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
    item1 = types.KeyboardButton("Анекдот")
    markup.add(item1)
    bot.send_message(m.chat.id,
                     'Нажми: \nАнекдот для получения интересного анекдота ',
                     reply_markup=markup)
```
#### Запускаем бота
```python
bot.polling(none_stop=True, interval=0)
```