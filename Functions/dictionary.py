import nltk
from deep_translator import GoogleTranslator
from nltk.corpus import wordnet

def translate_text(first_lang, second_lang, text):
    translator = GoogleTranslator(source=first_lang, target=second_lang)
    result = translator.translate(text)
    return result

def get_definition(word):
    word_ = translate_text('ru', 'en', word.lower())
    synsets = wordnet.synsets(word_)
    definitions = [syn.definition() for syn in synsets]

    if definitions:
        if len(definitions) > 3:
            translated_definitions = [translate_text('en', 'ru', el) for el in definitions[:3]]
        else:
            translated_definitions = [translate_text('en', 'ru', el) for el in definitions]

        return "\n" + '\n'.join([f'{k + 1}) {w.capitalize()}' for k, w in enumerate(translated_definitions)])
    return "\n(!) Ошибка, пожалуйста проверьте написание слова..."