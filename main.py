import time, telebot, config, button_setup, stickers_lib, random

# подключение к боту
bot = telebot.TeleBot(config.token)

# Словарь про команду
team = {'Настя': 'отвечает за поиск библеотек на начальном этапе, а затем будет помогать с тестами модулей',
        'Никита': 'ставит всё на сервер и работает с БД',
        'Коля': 'пишет код для этого бота'
        }


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, random.choice(stickers_lib.welcome_stickers_id))
    start_message = f"Привет, {message.from_user.first_name}!\nЧем могу быть полезен?"  # Обращаемся к пользователю по имени в telegram
    bot.send_message(message.chat.id, start_message, parse_mode='html', reply_markup=button_setup.button)


# Команда /team_info
@bot.message_handler(commands=['developers_info'])
def developers_info(message):
    for name in team:
        start_message = name + ' - ' + team[name]  # выводим словарь
        bot.send_message(message.chat.id, start_message)
        time.sleep(0.2)  # мини-зареджка в 2 мс. для отправки сообщений в цикле


# Команда /about
@bot.message_handler(commands=['about'])
def about(message):
    # Ниже выводим ключи из словаря team
    about_message = "*Я — учебный проект 3 ФКН-щиков*\nИх зовут — " + ', '.join(
        team.keys()) + '\n\n[Проект на GitHub](https://github.com/i9d/superbottelegramskoleyinastey)'
    bot.send_message(message.chat.id, about_message, parse_mode='markdown')


# Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    help_message = "Пока я могу только рассказать о проекте и нашей команде. Введи команду /about или /team_info"
    bot.send_message(message.chat.id, help_message)


# Модерация голосовых сообщений
@bot.message_handler(content_types=['voice'])
def get_voice(message):
    print('Пришло голосовое сообщение от', message.from_user.username)
    if (message.chat.id == config.group_id): delete_voise_message(message)
    else: bot.send_message(message.chat.id, 'Я не умею слушать, прости')


# Обработка запросов (документов, фото и текстовых сообщений)
@bot.message_handler(content_types=['text'])
def get_text(message):
    # обработка в консоль
    print('Пришло сообщение от', message.from_user.username + ':')
    print(message.text)

    if message.text == 'О проекте':
        about(message)
    elif message.text == 'Разработчики':
        developers_info(message)
    #else:
    #    bot.send_message(message.from_user.id, "Я пока не знаю что с этим делать. Попробуй написать /help")

# Когда бот получает стикер, будет отправлять случайные из stickers_lib.py
@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    print('Получен стикер от', message.from_user.username)  # обработка в консоль
    if (message.chat.id != config.group_id):
        bot.send_sticker(message.chat.id, random.choice(stickers_lib.stickers_id))

# Удаление голосовых сообщений с предупреждением отправителя
def delete_voise_message(message):
    warming_message = '@' + str(message.from_user.username) + ', голосовые сообщения запрещены. Не надо их сюда отправлять'
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, warming_message)
    print('Начинаю удалять сообщение')
    bot.send_message(message.chat.id, 'Я это пока просто удалю, а потом уже реализую бан.')

# Бот постоянно ждёт для себя сообщения
bot.polling(none_stop=True)
