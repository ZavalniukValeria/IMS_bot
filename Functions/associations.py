import random
import math
from Databases.words import read_db
from Levenshtein import distance as lev


def get_full_line(text):
    all_ = read_db()
    all_ = [el[1] for el in all_]

    def per_cent(main, might):
        return math.ceil(100 - (lev(main, might) / len(might)) * 100)

    def give(word, oldest):
        these, last = list(), ''
        for el in all_:
            if per_cent(word, el) >= 50:
                return f'{oldest} => {el}'
            if (per_cent(word, el) < 50) and (per_cent(word, el) >= 10):
                these.append(f'{per_cent(word, el)}{el}')
            else:
                last = el
        if these == []:
            return f'{oldest} ->> {last}'
        return f'{oldest} =>> {random.choice(these)[2:]}'

    d = {
        'а': ['а', 'a', '@'],
        'б': ['б', 'b'],
        'в': ['в', 'b', 'v'],
        'г': ['г', 'g'],
        'д': ['д', 'd'],
        'е': ['е', 'e', 'ё'],
        'ж': ['ж'],
        'з': ['з', 'z'],
        'и': ['и', 'i'],
        'й': ['й'],
        'к': ['к', 'k'],
        'л': ['л', 'l'],
        'м': ['м', 'm'],
        'н': ['н', 'n'],
        'о': ['о', 'o'],
        'п': ['п', 'p'],
        'р': ['р', 'r'],
        'с': ['с', 'c', 's'],
        'т': ['т', 't'],
        'у': ['у', 'y', 'u', 'w'],
        'ф': ['ф', 'f'],
        'х': ['х', 'x', 'h'],
        'ц': ['ц'],
        ' ': [' '],
        'ч': ['ч', 'ch'],
        'ш': ['ш', 'sh'],
        'щ': ['щ', 'sch'],
        'ь': ['ь', 'b'],
        'ы': ['ы', 'bi'],
        'ъ': ['ъ'],
        'э': ['э', 'e'],
        'ю': ['ю', 'io'],
        'я': ['я', 'ya']
    }

    def correct(line):
        line = line.lower()
        new = ''
        for q in line:
            if q in [' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л',
                     'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']:
                new += q
        return ' '.join(new.split())

    def transfer(get_text):
        def change_letter(beer):
            for key, value in d.items():
                for letter in value:
                    if letter == beer:
                        return key

        return ''.join([change_letter(item) for item in get_text])

    text = text.split()
    text = [correct(f) for f in text]
    old_text = text.copy()
    text = [transfer(w) for w in text]
    return [give(text[t], old_text[t]) for t in range(len(text))]
