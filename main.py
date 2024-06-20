import telebot
import datetime
import time
import threading
import random
from time import sleep

TOKEN = '7478222461:AAEx_6JUHX6ACbmQOBKId9GbZageNrdIvtQ'
user_data={}
name = ''
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    global user_data
    global name
    bot.reply_to(message, '*Привет!* Я чат-бот, который будет *напоминать тебе пить лекарства и водичку*!\n'
                          '*Познакомимся? Как зовут тебя?*', parse_mode="Markdown")
    bot.register_next_step_handler(message, get_name)
def get_name(message):
    global name
    if message.text is not None:
        name = str(message.text) + '! '
    bot.send_message(message.chat.id, f"*{name}Рад общению!* Введи нужную команду или /help", parse_mode="Markdown")

@bot.message_handler(commands=['stop'])
def stop_command_handler(message):
    global name
    if message.text == '/stop':
        bot.reply_to(message, f'*{name}До свидания!*\n_Работа с чат-ботом завершена._ \n*До новых встреч!*',
                     parse_mode="Markdown")


@bot.message_handler(commands=['set_remind'])
def set_remind(message):
    global user_data
    global name
    reminder_thread = threading.Thread(target=send_reminders, args=(message.chat.id,))
    reminder_thread.start()
    result = get_times_string(user_data)
    bot.reply_to(message, f'*{name}Отлично!* Напоминание о лекарствах в нужные часы (*{result}*) установлено.\n'
                          f'Введена следующая информация *о лекарствах и времени приёма*:\n'
                          f'*{user_data['morning_time']} ч.* - принять: *{user_data['morning_medicines']}*;\n'
                          f'*{user_data['day_time']} ч.* - принять: *{user_data['day_medicines']}*;\n'
                          f'*{user_data['evening_time']} ч.* - принять: *{user_data['evening_medicines']}*;\n'
                          f'*{user_data['night_time']} ч.* - принять: *{user_data['night_medicines']}*.',
                 parse_mode="Markdown")
    # reminder_thread.start()


@bot.message_handler(commands=['check_info'])
def check_info(message):
    # print(message.chat.id)
    global user_data
    global name
    if user_data is None:
        bot.reply_to(message, f'*{name}Напоминание* о лекарствах в нужные часы *не введено*\n'
                              f'*Импортируем ранее введенные из файла*', parse_mode="Markdown")
        user_data = import_from_file('med.txt')
        result = get_times_string(user_data)
        # bot.send_message(message.chat.id, f"Спасибо! Напоминание о лекарствах в нужные часы ({result}) установлено.")
        bot.reply_to(message, f'{name}Напоминание о лекарствах в нужные часы (*{result}*) готово к установке.\n'
                              f'Введена следующая информация *о лекарствах и времени приёма*:\n'
                              f'*{user_data['morning_time']} ч.* - принять: *{user_data['morning_medicines']}*;\n'
                              f'*{user_data['day_time']} ч.* - принять: *{user_data['day_medicines']}*;\n'
                              f'*{user_data['evening_time']} ч.* - принять: *{user_data['evening_medicines']}*;\n'
                              f'*{user_data['night_time']} ч.* - принять: *{user_data['night_medicines']}*.',
                     parse_mode="Markdown")
        bot.send_message(message.chat.id,
                         f"{name}Для установки напоминаний не забудь дать команду /set_remind")
    else:
        # user_data = import_from_file('med.txt')
        result = get_times_string(user_data)
    # bot.send_message(message.chat.id, f"Спасибо! Напоминание о лекарствах в нужные часы ({result}) установлено.")
        bot.reply_to(message, f'{name}Напоминание о лекарствах в нужные часы (*{result}*) готово к установке.\n'
                  f'Имеется следующая информация *о лекарствах и времени приёма*:\n'
                 f'*{user_data['morning_time']} ч.* - принять: *{user_data['morning_medicines']}*;\n'
                 f'*{user_data['day_time']} ч.* - принять: *{user_data['day_medicines']}*;\n'
                 f'*{user_data['evening_time']} ч.* - принять: *{user_data['evening_medicines']}*;\n'
                 f'*{user_data['night_time']} ч.* - принять: *{user_data['night_medicines']}*.', parse_mode="Markdown")
        bot.send_message(message.chat.id,
                         f"{name}Для установки напоминаний не забудь дать команду /set_remind")

@bot.message_handler(commands=['erase_info'])
def erase_info(message):
    global name
    global user_data
    user_data.clear()
    bot.send_message(message.chat.id, f"*{name}Не забудьте, при необходимости, ввести* перечень лекарств со временем их приема", parse_mode="Markdown")

@bot.message_handler(commands=['fact'])
def fact_message(message):
    global name
    list = [
        "*Вода на Земле может быть старше самой Солнечной системы:* Исследования показывают, что от 30% до 50% воды в наших океанах возможно присутствовала в межзвездном пространстве еще до формирования Солнечной системы около 4,6 миллиарда лет назад.",
        "*Горячая вода замерзает быстрее холодной:* Это явление известно как эффект Мпемба. Под определенными условиями горячая вода может замерзать быстрее, чем холодная, хотя ученые до сих пор полностью не разгадали механизм этого процесса.",
        "*Больше воды в атмосфере, чем во всех реках мира:* Объем водяного пара в атмосфере Земли в любой момент времени превышает объем воды во всех реках мира вместе взятых. Это подчеркивает важную роль атмосферы в гидрологическом цикле, перераспределяя воду по планете.",
        "*Прием воды помогает организму правильно функционировать*, поддерживая оптимальный уровень гидратации клеток и органов.",
        "*Вода ускоряет метаболизм и помогает организму расщеплять лекарства*, что способствует более быстрому и эффективному действию препаратов.",
        "**Пить воду во время приема лекарств помогает предотвратить раздражение желудка* и уменьшить возможные побочные эффекты.",
        "*Употребление достаточного количества воды помогает организму избавляться от токсинов и отходов*, что может улучшить эффективность лекарственной терапии.",
        "*Вода также улучшает усвоение питательных веществ из лекарств*, улучшая их действие и помогая быстрее восстановиться от болезни или травмы.",
        "*Своевременное прием лекарств помогает быстрее и эффективнее справиться* с заболеванием или состоянием здоровья.",
        "*Правильно принимаемые лекарства* могут предотвратить осложнения и улучшить прогноз заболевания.",
        "*Регулярное применение лекарств по указанию врача* помогает контролировать хронические заболевания и поддерживать состояние здоровья на оптимальном уровне.",
        "*Прием лекарств вовремя* может снизить риск развития осложнений и ускорить процесс выздоровления.",
        "*Правильно принимаемые лекарства могут улучшить качество жизни*, снизить симптомы заболевания и улучшить общее самочувствие."]
    random_fact = random.choice(list)
    bot.reply_to(message, f'*{name}Лови факт о воде*\n {random_fact}', parse_mode="Markdown")

# Словарь для хранения данных о лекарствах и времени приема

# Функция для запроса информации о приеме лекарств в разное время суток
# Пользователь может информацию подготовить в файле и способом copy-paste загружать в бот на соответствующие запросы
@bot.message_handler(commands=['vvod_info'])
def vvod_info(message):
    global user_data
    bot.send_message(message.chat.id, "*Введи перечень лекарств для приема утром*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_morning_info)
def get_morning_info(message):
    user_data['morning_medicines'] = message.text
    # user_data = {'morning_medicines': message.text}
    bot.send_message(message.chat.id, "*Введи утреннее время приема лекарств (например, 08:00)*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_morning_time)
def get_morning_time(message):
    user_data['morning_time'] = message.text
    bot.send_message(message.chat.id, "*Введи перечень лекарств для приема днём*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_day_info)
def get_day_info(message):
    user_data['day_medicines'] = message.text
    bot.send_message(message.chat.id, "*Введи дневное время приема лекарств (например, 13:00)*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_day_time)
def get_day_time(message):
    user_data['day_time'] = message.text
    bot.send_message(message.chat.id, "*Введи перечень лекарств для приема вечером*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_evening_info)
def get_evening_info(message):
    user_data['evening_medicines'] = message.text
    bot.send_message(message.chat.id, "*Введи вечернее время приема лекарств (например, 19:00)*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_evening_time)
def get_evening_time(message):
    user_data['evening_time'] = message.text
    bot.send_message(message.chat.id, "*Введи перечень лекарств для приема на ночь*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_night_info)
def get_night_info(message):
    user_data['night_medicines'] = message.text
    bot.send_message(message.chat.id, "*Введи время приема лекарств на ночь (например, 23:00)*:", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_night_time)
def get_night_time(message):
    global name
    user_data['night_time'] = message.text
    result = get_times_string(user_data)
    bot.send_message(message.chat.id, f'*{name}Спасибо!* Напоминание о лекарствах в нужные часы (*{result}*) подготовлено.\n'
                 f'Введена следующая информация *о лекарствах и времени приёма*:\n'
                                      # f'{user_data}')
                 f'*{user_data['morning_time']} ч.* - принять: *{user_data['morning_medicines']}*;\n'
                 f'*{user_data['day_time']} ч.* - принять: *{user_data['day_medicines']}*;\n'
                 f'*{user_data['evening_time']} ч.* - принять: *{user_data['evening_medicines']}*;\n'
                 f'*{user_data['night_time']} ч.* - принять: *{user_data['night_medicines']}*.', parse_mode="Markdown")

def get_times_string(user_data):
    time_values = [value for key, value in user_data.items() if key.endswith('_time')]
    return ', '.join(time_values)

# Функция для загрузки справочной информации из файла
def get_bot_description(file_name = 'about_bot.txt'):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "Файл не найден."
# Обработчик команды /about
@bot.message_handler(commands=['about'])
def send_about(message):
    about_info = get_bot_description()
    bot.send_message(message.chat.id, about_info, parse_mode="Markdown")
def load_help_info():
    with open('help_bot.txt', 'r', encoding="utf-8") as file:
        help_text = file.read()
    return help_text
# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    help_info = load_help_info()
    bot.send_message(message.chat.id, help_info)
# Обработчик команды /?
@bot.message_handler(commands=['?'])
def send_help(message):
    help_info = load_help_info()
    bot.send_message(message.chat.id, help_info)
def send_reminders(chat_id):
    global user_data
    global name
    morning_rem = user_data['morning_time']
    day_rem = user_data['day_time']
    evening_rem = user_data['evening_time']
    night_rem = user_data['night_time']
    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == morning_rem:
            bot.send_message(chat_id, f"*{name}Напоминание {user_data['morning_time']} ч.* - выпей лекарства:\n"
                                      f" *{user_data['morning_medicines']}* \n"
                                      f"_и запей стаканом воды_", parse_mode="Markdown")
            time.sleep(61)
        elif now == day_rem:
            bot.send_message(chat_id, f"*{name}Напоминание {user_data['day_time']} ч.* - выпей лекарства:\n"
                                      f" *{user_data['day_medicines']}* \n"
                                      f"_и запей стаканом воды_", parse_mode="Markdown")
            time.sleep(61)
        elif now == evening_rem:
            bot.send_message(chat_id, f"*{name}Напоминание {user_data['evening_time']} ч.* - выпей лекарства:\n"
                                      f" *{user_data['evening_medicines']}* \n"
                                      f"_и запей стаканом воды_", parse_mode="Markdown")
            time.sleep(61)
        elif now == night_rem:
            bot.send_message(chat_id, f"*{name}Напоминание {user_data['night_time']} ч.* - выпей лекарства:\n"
                                      f" *{user_data['night_medicines']}* \n"
                                      f"_и запей стаканом воды_", parse_mode="Markdown")
            time.sleep(61)
        time.sleep(1)
def export_to_file(user_data, file_name='med.txt'):
    with open(file_name, 'w', encoding="utf-8") as file:
        for key, value in user_data.items():
            file.write(f'{key}: {value}\n')

@bot.message_handler(commands=['export_data'])
def export_data(message):
    global user_data
    global name
    export_to_file(user_data, 'med.txt')
    bot.send_message(message.chat.id, f'*{name}Записан введённый массив данных в файл "med.txt"*',
                     parse_mode="Markdown")
def import_from_file(file_name='med.txt'):
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            for line in file:
                key, value = line.strip().split(': ')
                user_data[key] = value
        return user_data
    except FileNotFoundError:
        print(f'File {file_name} not found')
        return {}
@bot.message_handler(commands=['import_data'])
def import_data(message):
    global user_data
    global name
    user_data = import_from_file('med.txt')
    print(f'Данные импортированы: {user_data}')
    bot.send_message(message.chat.id,
                     f'{name}Загружен из файла *"med.txt"* сохраненный ранее в этот файл массив данных.\n'
                          f'Проверь это командой */check_info*', parse_mode="Markdown")

@bot.message_handler(commands=['edit_file'])
def edit_file(message):
    global name
    file_path = 'med.txt'
    # Открываем файл для редактирования
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        bot.send_message(message.chat.id,f"Текущее содержимое файла:\n"
                                         f"{content}")
        bot.send_message(message.chat.id, "*Введи новое содержимое файла*:", parse_mode="Markdown")
        bot.register_next_step_handler(message, get_new_content)
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print("Произошла ошибка:", e)

def get_new_content(message):
    global name
    file_path = 'med.txt'
    new_content = message.text
    print(new_content)
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(new_content)
    bot.send_message(message.chat.id,
                         f'{name}Отредактирован файл *"med.txt"*.\n'
                         f'Загрузи данные в чат-бот командой */import_data*\n'
                         f'и потом проверь результат командой */check_info*', parse_mode="Markdown")

bot.polling(none_stop=True)
# bot.infinity_polling(none_stop=True, timeout=10, long_polling_timeout = 5)

# while True:
#     try:
#         bot.polling(none_stop=True, timeout=10, long_polling_timeout = 5)
#     except Exception as _ex:
#         print(_ex)
#         sleep(15)

# if __name__=='__main__':
# while True:
#     try:
#         bot.polling(non_stop=True, interval=0)
#     except Exception as e:
#         print(e)
#         time.sleep(5)
#         continue


# Обработчик команды /stop
# def stop(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Bot is stopping...")
#     # Остановка работы бота
#     context.bot.stop()
#
#
# # Создание Updater и добавление обработчиков команд
# updater = Updater("TOKEN", use_context=True)
# updater.dispatcher.add_handler(CommandHandler("start", start))
# updater.dispatcher.add_handler(CommandHandler("stop", stop))
#
# # Запуск бота
# updater.start_polling()
# updater.idle()








# Рекомендуем создать команду help.
# Теперь ты можешь:
# попробовать придумать какие-то команды самостоятельно;
# усовершенствовать эту программу и додумать для нее дополнительный функционал.
# Попробуй доработать этот кейс по-своему. Чем больше необычных вещей ты в него внесешь, тем лучше будет проект.