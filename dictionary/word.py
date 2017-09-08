import click
from wordnik import *

from .utils import create_word_api, load_api_key

class Word(object):
    def __init__(self, word):
        self.word = word
        self._meanings = None
        self._examples = None
        self._hyphenation = None
        self._audio = None
        self._text_pronunciations = None
        self._phrases = None
        self._synonyms = None
        self._antonyms = None

    def __repr__(self):
        return 'Word({})'.format(self.word)

    @property
    def meanings(self):
        if self._meanings is None:
            self._meanings = Word.get_meanings(self.word)

        return self._meanings

    @property
    def examples(self):
        if self._examples is None:
            self._examples = Word.get_examples(self.word)

        return self._examples

    @property
    def hyphenation(self):
        if self._hyphenation is None:
            self._hyphenation = Word.get_hyphenation(self.word)

        return self._hyphenation

    @property
    def audio(self):
        if self._audio is None:
            self._audio = Word.get_audio(self.word)

        return self._audio

    @property
    def text_pronunciations(self):
        if self._text_pronunciations is None:
            self._text_pronunciations = Word.get_text_pronunciations(self.word)

        return self._text_pronunciations

    @property
    def phrases(self):
        if self._phrases is None:
            self._phrases = Word.get_phrases(self.word)

        return self._phrases

    @property
    def synonyms(self):
        if self._synonyms is None:
            self._synonyms = Word.get_synonyms(self.word)

        return self._synonyms

    @property
    def antonyms(self):
        if self._antonyms is None:
            self._antonyms = Word.get_antonyms(self.word)

        return self._antonyms

    @staticmethod
    def get_meanings(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        definitions = WORD_API.getDefinitions(word, limit=5)
        data = [definition.text for definition in definitions]
        return data

    @staticmethod
    def get_examples(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        examples = WORD_API.getExamples(word, limit=3)
        return [example.text for example in examples.examples]

    @staticmethod
    def get_hyphenation(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        hyphenation = WORD_API.getHyphenation(word)
        if hyphenation is not None:
            return '-'.join(syllable.text for syllable in hyphenation)

        return hyphenation

    @staticmethod
    def get_audio(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        audio = WORD_API.getAudio(word, limit=1)
        # TODO: Provide flexibility in setting limit
        if audio is not None:
            return audio[0].fileUrl
        else:
            return None

    @staticmethod
    def get_text_pronunciations(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        pronunciations = WORD_API.getTextPronunciations(word)
        return [pronunciation.raw for pronunciation in pronunciations
                                  if pronunciation.rawType != 'arpabet']

    @staticmethod
    def get_phrases(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        phrases = WORD_API.getPhrases(word)
        if phrases is not None:
            return ['{} {}'.format(phrase.gram1, phrase.gram2) for phrase in phrases]
        else:
            return phrases

    @staticmethod
    def get_synonyms(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        synonyms = WORD_API.getRelatedWords(word, relationshipTypes='synonym')
        if synonyms is not None:
            synonym_words = []
            for synonym in synonyms:
                if synonym.relationshipType == 'synonym':
                    synonym_words.extend(synonym.words)
               
            return synonym_words

        return None

    @staticmethod
    def get_antonyms(word):
        API_KEY = load_api_key()
        WORD_API = create_word_api(API_KEY)
        antonyms = WORD_API.getRelatedWords(word, relationshipTypes='antonym')
        if antonyms is not None:
            antonym_words = []
            for antonym in antonyms:
                if antonym.relationshipType == 'antonym':
                    antonym_words.extend(antonym.words)

            return antonym_words

        return None
        
    def stringify(self):

        # Representation for meanings
        meanings = list()
        for index, meaning in enumerate(self.meanings, start=1):
            meanings.append(click.style('{}. {}'.format(index, meaning)))
        
        # Representation for examples
        examples = list()
        for index, example in enumerate(self.examples, start=1):
            examples.append(click.style('{}. {}'.format(index, example), fg='cyan'))
        
        hyphenation, audio, phrases, text_pronunciations = None, None, None, None
        
        if self.hyphenation is not None:
            hyphenation = click.style(self.hyphenation, fg='green')
        
        if self.audio is not None:
            audio = click.style(self.audio, bg='black')

        # Representation for text pronunciations
        if self.text_pronunciations is not None:
            text_pronunciations = list()
            for index, pronunciation in enumerate(self.text_pronunciations, start=1):
                text_pronunciations.append(click.style('{}. {}'.format(index, pronunciation), fg='yellow'))

        # Representation for phrases
        if self.phrases is not None:
            phrases = list()
            for index, phrase in enumerate(self.phrases, start=1):
                phrases.append(click.style('{}. {}'.format(index, phrase), fg='magenta'))
        
        # Representation for synonyms
        synonyms, antonyms = None, None
        if self.synonyms is not None:
            synonyms = click.style(', '.join(self.synonyms), fg='green')

        if self.antonyms is not None:
            antonyms = click.style(', '.join(self.antonyms), fg='red')

        headings = [
                    ('Word', click.style(self.word, fg='red', bold=True), '\t'),
                    ('Meanings', meanings, '\n'), 
                    ('Synonyms', synonyms, ' '),
                    ('Antonyms', antonyms, ' '),
                    ('Examples', examples, '\n'), 
                    ('Text Pronunciations', text_pronunciations, '\n'),
                    ('Phrases', phrases, '\n'),
                    ('Hyphenation', hyphenation, ' '),
                    ('Audio', audio, ' ')
                    ]

        s = [create_entry(heading, data, separator) for heading, data, separator in headings if data is not None]

        return '\n\n'.join(s)

def create_entry(heading, data, separator):
    HEADING_COLOR = 'blue'
    complete_heading = heading + ':'

    if isinstance(data, list):
        complete_data = '\n'.join(data)
    else:
        complete_data = data

    #print('Printing:', heading)
    #print('DATA:', data)
    return click.style(complete_heading, fg=HEADING_COLOR, underline=True, bold=True) + separator + complete_data
