"""
Main class for joji logic
"""
import os
import pickle
import emoji
import spacy
from keybert import KeyBERT

try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    print("Downloading language model for spacy (don\'t worry, this will only happen once)")
    from spacy.cli import download
    download('en_core_web_md')
    nlp = spacy.load('en_core_web_md')

ALL_STOPWORDS = nlp.Defaults.stop_words

emoji_dict_path = os.path.join(
    os.path.dirname(__file__),
    "data/emoji_dict1.p"
)
infile = open(emoji_dict_path, 'rb')
emoji_dict = pickle.load(infile)
infile.close()


class Jojify(object):
    """
    class containing methods to map text to emoji
    """
    emoji_dict = emoji_dict
    kw_model = KeyBERT()

    @staticmethod
    def generate_unicode(emoj):
        """
        Generate unicode
        """
        return f'U+{ord(emoj):X}' if len(emoj) == 1 else None

    @classmethod
    def _simple_check(cls, text):
        """
        Direct search of emoji
        """
        emoji_data, score = None, 0.0
        if text in cls.emoji_dict:
            score = 1.0
            emoji_data = cls.emoji_dict.get(text)
        return emoji_data, score

    @classmethod
    def _sentence_check(cls, text):
        """
        Direct search for emoji in sentence
        """
        #words = text.split(" ")
        _, keywords = cls.extract(text)
        keywords = cls.filter_keywords(keywords)
        for word, score in keywords:
            emoji_data, score = cls._simple_check(word)
            if score == 1.0:
                return emoji_data, score
        return None, 0.0

    @staticmethod
    def _similarity_match(vector1, vector2):
        return vector1.similarity(vector2)

    @staticmethod
    def get_vector(emoji_data):
        """
        get nlpfied obj
        """
        return emoji_data.get("vector")

    @classmethod
    def _context_similarity_check(cls, text):
        max_score = 0  # set threshold value instead
        max_emoji_data = None
        text = nlp(text)
        for emoji_name in cls.emoji_dict:
            emoji_data = cls.emoji_dict.get(emoji_name)
            vector = cls.get_vector(emoji_data)
            if vector.vector_norm and text.vector_norm:
                score = cls._similarity_match(text, vector)
            else:
                score = 0
            if score > max_score:
                max_score = score
                max_emoji_data = emoji_data
        return max_emoji_data, max_score

    @staticmethod
    def remove_stop_words(text):
        """
        Remove stop words from text
        """
        text_tokens = text.split(" ")
        words = [
            word for word in text_tokens if not word in ALL_STOPWORDS
        ]
        return words

    @classmethod
    def sentence_context_check(cls, text):
        """
        Context check in sentence
        """
        score = 0
        data = {}
        #words = cls.remove_stop_words(text)
        _, keywords = cls.extract(text)
        keywords = cls.filter_keywords(keywords)
        for word, _ in keywords:
            emoji_data, predict_score = cls._context_similarity_check(
                word
            )
            if predict_score > score:
                score = predict_score
                data = emoji_data
        return data, score

    @staticmethod
    def get_short_name(emoji_data):
        """
        Get short name of emoji
        """
        return emoji_data.get("short_name")

    @classmethod
    def get_emoji_and_unicode(cls, emoji_data):
        """
        Get emoji and unicode
        """
        short_name = cls.get_short_name(emoji_data)
        max_emoji = emoji.emojize(short_name)
        max_unicode = cls.generate_unicode(max_emoji)
        return max_emoji, max_unicode

    @staticmethod
    def preprocess(text):
        """
        Preprocess text
        """
        text = text.lower()
        return text

    @classmethod
    def word_or_sentence_logic(cls, text):
        """
        Sentence split logic code
        """
        if len(text.split(" ")) > 1:
            emoji_data, score = cls._sentence_check(
                text
            )
            if not emoji_data:
                emoji_data, score = cls.sentence_context_check(
                    text
                )
        else:
            emoji_data, score = cls._simple_check(
                text
            )
            if not emoji_data:
                emoji_data, score = cls._context_similarity_check(
                    text
                )
        return emoji_data, score

    @classmethod
    def sentence_logic(cls, text):
        """
        Sentence processing logic for
        emoji prediction
        """
        emoji_data, score = cls._simple_check(
            text
        )
        if not emoji_data:
            emoji_data, score = cls._context_similarity_check(
                text
            )
        return emoji_data, score

    @classmethod
    def predict(cls, text):
        """
        Logic to predict the emoji
        """
        text = cls.preprocess(text)
        emoji_data, score = cls.word_or_sentence_logic(text)
        max_emoji, max_unicode = cls.get_emoji_and_unicode(emoji_data)
        return (max_emoji, max_unicode, score) if score else text
    
    @staticmethod
    def combine_keywords(text, keywords):
        """
        Combine keywords to form a sentence
        """
        strings, combine_keyword = [], ""
        words = text.lower().split()
        keywords = [
            i for i, j in keywords
        ]
        for _, word in enumerate(words):
            if word in keywords:
                combine_keyword = " ".join(
                    [
                        combine_keyword, word
                    ]
                )
            else:
                if combine_keyword:
                    strings.append(
                        combine_keyword.strip()
                    )
                combine_keyword = ""
        if combine_keyword:
            strings.append(
                combine_keyword.strip()
            )
        return strings
    

    @classmethod
    def extract(cls, text, combine=False):
        """
        extract logic for keywords
        """
        keywords = cls.kw_model.extract_keywords(
            text
        )
        if combine:
            keywords = cls.combine_keywords(
                text, keywords
            )
        return text, keywords
    
    @staticmethod
    def filter_keywords(keywords, threshold=0.5):
        """
        Filter keywords based on a threshold
        """
        return [
            (i, j) for i, j in keywords if j > threshold
        ]
    


