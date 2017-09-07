from wordnik import *

from .utils import create_word_api, load_api_key

class Word(object):
    def __init__(self, word):
        self.word = word


    @property
    def definitions(self):
        return Word.get_definitions(self.word)
        
    @property
    def examples(self):
        return Word.get_examples(self.word)
        
    @property
    def hyphenation(self):
        return Word.get_hyphenation(self.word)

    def __repr__(self):
        return 'Word({})'.format(self.word)

    @staticmethod
    def get_definitions(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        definitions = WORD_API.getDefinitions(word, limit=5)
        data = [definition.text for definition in definitions]
        return data

    @staticmethod
    def get_examples(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        examples = WORD_API.getExamples(word, limit=5)
        return [example.text for example in examples.examples]

    @staticmethod
    def get_hyphenation(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        hyphenation = WORD_API.getHyphenation(word)
        return '-'.join(syllable.text for syllable in hyphenation)
