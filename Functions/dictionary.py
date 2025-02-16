import nltk
# nltk.download('wordnet')
from googletrans import Translator
from nltk.corpus import wordnet

def translate_text(first_lang, second_lang, text):
    translator = Translator()
    result = translator.translate(text, src=first_lang, dest=second_lang)
    return result.text

def get_definition(word):
    word_ = translate_text('ru', 'en', word)
    synsets = wordnet.synsets(word_)
    definitions = [syn.definition() for syn in synsets]

    if len(definitions) > 3:
        translated_definitions = [translate_text('en', 'ru', el) for el in definitions[:3]]
    else:
        translated_definitions = [translate_text('en', 'ru', el) for el in definitions]

    return "\n" + '\n'.join([f'{k + 1}) {w.capitalize()}' for k, w in enumerate(translated_definitions)])


