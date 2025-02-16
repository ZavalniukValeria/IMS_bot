import telebot, random, time
from Databases.database import find_user_id_by_tg_id, get_user_by_id






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
        return bot.send_message(message.chat.id, "Числа закончились...")
    item, correct_answer = cases[case_id]
    bot.send_message(message.chat.id, f"Необходимо ответить на: {int(item) + 1}")
    bot.register_next_step_handler(message, lambda x: check_case(bot, x, cases, case_id, correct_answer))


def make_right(list_, how_many):
    new = dict()
    for k, el in enumerate(list_):
        new[k] = f'{el}'
    return new


def new_cmd_memo_get(bot, message):
    user_data = list(get_user_by_id(find_user_id_by_tg_id(int(message.from_user.id))))
    new_numbers = [str(random.randint(0, 100)) for _ in range(user_data[3])]
    content = make_right(new_numbers, int(user_data[3]))
    job = ' | '.join(new_numbers)
    first_message = bot.send_message(message.chat.id, f"{job}")
    time.sleep(int(user_data[2]) * len(content))
    bot.delete_message(message.chat.id, first_message.message_id)
    bot.send_message(message.chat.id, f"Начинаем!!")
    contents = list()
    for item in content.keys():
        contents.append((str(item).capitalize(), content[item].capitalize()))
    give_case(bot, message, contents, 0)

