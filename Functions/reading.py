import random
from Databases.words import read_db2



def reversed_reading(bot, msg):
    text = random.choice(list(read_db2()))[1]
    text = str(text)
    output = list()
    for word in text.split():
        addition = ""
        if word[-1] in ",.?!":
            addition = word[-1]
            word = word[:-1]
        output.append(word[::-1] + addition)
    bot.register_next_step_handler(
        bot.reply_to(msg, " ".join(output)),
        lambda x: bot.reply_to(x, f"Текст: {text}")
    )

def without_vowel(bot, msg):
    text = random.choice(list(read_db2()))[1]
    text = str(text)
    output = str()
    for letter in text:
        if letter.lower() not in "аеёиоуыэюя":
            output += letter

    bot.register_next_step_handler(
        bot.reply_to(msg, output),
        lambda x: bot.reply_to(x, f"Текст: {text}")
    )


def half_digits(bot, msg):
    text = random.choice(list(read_db2()))[1]
    text = str(text)
    output = str()
    for letter in text:
        if letter.lower() not in " !.,?-–":
            if random.choice([1, 0]) or letter not in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя":
                output += letter
            else:
                output += str(1 + "абвгдеёжзийклмнопрстуфхцчшщъыьэюя".index(letter.lower())) + ";"
        else:
            output += letter
    bot.register_next_step_handler(
        bot.reply_to(msg, output),
        lambda x: bot.reply_to(x, f"Текст: {text}")
    )
