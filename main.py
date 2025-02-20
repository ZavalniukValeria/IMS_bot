import telebot
from telebot import types
from Functions.dictionary import get_definition
from Functions.training import training
from Functions.reading import reversed_reading, without_vowel, half_digits
from Functions.memory_numbers import new_cmd_memo_get
from Functions.associations import get_full_line
from Databases.important import give_info
from Databases.database import create_table, add_user
from Functions.user_settings import get_changes


bot = telebot.TeleBot(give_info('token'))


@bot.message_handler(commands=['start'])
def main(msg):
    create_table()
    add_user(int(msg.from_user.id), 10, 5, 10, 5)
    bot.reply_to(msg, "Выберите режим работы", reply_markup=get_keyboard(empty=False))


@bot.message_handler(func=lambda message: 'mini app' in message.text.lower())
def handle_github(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Открыть mini app", web_app=types.WebAppInfo(url=give_info('url')))
    markup.add(button)


    bot.send_message(
        message.chat.id,
        f"{message.from_user.first_name}! Вот mini app, где Вы сможете узнать, как всё работает!",
        reply_markup=markup
    )


@bot.message_handler(content_types=['text'])
def get_text(msg):
    match msg.text.lower():
        case "толкование терминов":
            bot.register_next_step_handler(
                bot.reply_to(msg, 'Введите слово, значение которого хотите узнать', reply_markup=get_keyboard(empty=True)),
                lambda x: bot.reply_to(x, "Определение: " + str(get_definition(x.text)))
            )
        case "ассоциации":
            bot.register_next_step_handler(
                bot.reply_to(msg, 'Введите слово(а), ассоциацию(ии) к которому(ым) хотите получить', reply_markup=get_keyboard(empty=True)),
                lambda x: bot.reply_to(x, f"Результат:\n{'\n'.join(get_full_line(x.text))}")
            )
        case "числа":
            new_cmd_memo_get(bot, msg)
        case "скорочтение":
            bot.reply_to(msg, "Выберите раздел для тренировки", reply_markup=get_keyboard(['Чтение наоборот', 'Чтение без гласных', 'Слова полуцифры', 'В начало']))
        case _ if msg.text.lower() == "далее" or msg.text.lower() == "в начало":
                bot.reply_to(msg, "Выберите раздел для тренировки",
                 reply_markup=get_keyboard(['Толкование терминов', 'Числа', 'Ассоциации', 'Скорочтение', 'Слова', 'Назад']))
        case "настройки":
            bot.reply_to(msg, "Вы можете выбрать одну из опций", reply_markup=get_keyboard(settings=True))
        case "назад":
            main(msg)
        case "чтение наоборот":
            reversed_reading(bot, msg)
        case "чтение без гласных":
            without_vowel(bot, msg)
        case "слова полуцифры":
            half_digits(bot, msg)
        case "слова":
            training(bot, msg)
        case _:
            get_changes(bot, msg, msg.from_user.id)


def get_keyboard(custom_markup: list=None, settings: bool=False, empty: bool=True):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    if not empty:
        keyboard.add(
            telebot.types.KeyboardButton(text="Настройки"),
            telebot.types.KeyboardButton(text="Далее"),
            telebot.types.KeyboardButton(text="mini app"),
        )
    if custom_markup:
        keyboard.add(*custom_markup)
    if settings:
        keyboard.row(
            telebot.types.KeyboardButton(text="время -> чисел"),
            telebot.types.KeyboardButton(text="кол-во -> чисел")
        )
        keyboard.row(
            telebot.types.KeyboardButton(text="время -> слов"),
            telebot.types.KeyboardButton(text="кол-во -> слов")
        )
        keyboard.row(
            telebot.types.KeyboardButton(text="Назад"),
        )
    return keyboard


if __name__ == "__main__":
    bot.polling(none_stop=True)