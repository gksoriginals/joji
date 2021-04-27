import os
import json
import spacy
try:
  nlp = spacy.load("en_core_web_md")
except OSError:
  print("Downloading language model for spacy (don\'t worry, this will only happen once)")
  from spacy.cli import download
  download('en_core_web_md')
  nlp = spacy.load('en_core_web_md')

emoji_dict_path = "/data/emoji_dict.json"
emoji_dict = open(emoji_dict_path)
emoji_dict = json.load(emoji_dict)

class Jojify(object):
  """
  class containing methods to map text to emoji
  """  
  emoji_dict = emoji_dict
  
  @classmethod
  def _simple_check(cls, text):
    if text in cls.emoji_dict:
      return cls.emoji_dict.get(text)
    return None
  
  @staticmethod
  def _similarity_match(word1, word2):
      word1 = nlp(word1)
      word2 = nlp(word2)
      return word1.similarity(word2)
    
  @classmethod  
  def _context_similarity_check(cls, text):
    max_score = 0 # set threshold value instead
    max_emoji = None
    for emoji_name in cls.emoji_dict:
      score = cls._similarity_match(text, emoji_name)
      if score > max_score:
        max_emoji = cls.emoji_dict.get(emoji_name)
   return max_emoji, max_score

  @classmethod
  def predict(cls, text):
    emoji = cls._simple_check(text)
    emoji = cls._context_similarity_check(text) if not emoji else emoji
    return emoji if emoji else else text
  
 
  
