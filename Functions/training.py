import random
import time
from Databases.database import find_user_id_by_tg_id, get_user_by_id
from Databases.words import read_db



def dict_to_list(d):
    return [f"{int(key) + 1} - {value}" for key, value in d.items()]



def check_case(bot, x, cases, case_id, correct_answer):
    if x.text.lower() != "/конец":
        bot.send_message(x.chat.id,
                         "Удачно!" if x.text.lower() == correct_answer.lower() else f"Не-не. Правильно: {correct_answer}")
        give_case(bot, x, cases, case_id + 1)
    else:
        bot.send_message(x.chat.id, "Ну ладно :((")


def give_case(bot, message, cases, case_id):
    if case_id >= len(cases):
        return bot.send_message(message.chat.id, "Слова закончились...")
    item, correct_answer = cases[case_id]
    bot.send_message(message.chat.id, f"Необходимо ответить на: {int(item) + 1}")
    bot.register_next_step_handler(message, lambda x: check_case(bot, x, cases, case_id, correct_answer))


def make_right(list_, how_many):
    new = dict()
    for k, el in enumerate(range(1, how_many + 1)):
        new[k] = f'{random.choice(list_)}'
    return new


def training(bot, message):
    words_all = read_db()
    words_all = [str(el[1]) for el in words_all]
    user_data = list(get_user_by_id(find_user_id_by_tg_id(int(message.from_user.id))))
    content = make_right(words_all, int(user_data[5]))
    job = '\n'.join(dict_to_list(content))
    first_message = bot.send_message(message.chat.id, f"{job}")
    time.sleep(int(user_data[4]) * len(content))
    bot.delete_message(message.chat.id, first_message.message_id)
    bot.send_message(message.chat.id, f"Начинаем!")
    contents = list()
    for item in content.keys():
        contents.append((str(item).capitalize(), content[item].capitalize()))
    give_case(bot, message, contents, 0)