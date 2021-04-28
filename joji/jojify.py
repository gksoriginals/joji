import os
import emoji
import json
import emoji
import spacy
import pickle
import numpy as np
from numba import jit

try:
  nlp = spacy.load("en_core_web_md")
except OSError:
  print("Downloading language model for spacy (don\'t worry, this will only happen once)")
  from spacy.cli import download
  download('en_core_web_md')
  nlp = spacy.load('en_core_web_md')

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

  @staticmethod
  def generate_unicode(emoj):
    return f'U+{ord(emoj):X}' if len(emoj) == 1 else emoj
  
  @classmethod
  def _simple_check(cls, text):
    if text in cls.emoji_dict:
      emoji_ = emoji.emojize(cls.emoji_dict.get(text).get("short_name"))
      return (
        emoji_,
        cls.generate_unicode(emoji_),
        1
      )
    return None
  
  @staticmethod
  def _similarity_match(word1, word2):
    word1 = nlp(word1)
    return word1.similarity(word2)

  @classmethod
  def _similarity_match_1(cls, word1, word2):
    word1 = nlp(word1)
    return cls.cosine_similarity_numba(word1.vector, word2.vector)

    
  @classmethod  
  def _context_similarity_check(cls, text):
    max_score = 0 # set threshold value instead
    max_emoji = None
    for emoji_name in cls.emoji_dict:
      score = cls._similarity_match(text, emoji_dict.get(emoji_name).get("vector"))
      if score > max_score:
        max_emoji = emoji.emojize(cls.emoji_dict.get(emoji_name).get("short_name"))
        max_score = score
    max_unicode = cls.generate_unicode(max_emoji)
    return max_emoji, max_unicode, max_score


  @staticmethod
  def preprocess(text):
    text = text.lower()
    return text

  @classmethod
  def predict(cls, text):
    text = cls.preprocess(text)
    emoji = cls._simple_check(text)
    emoji = cls._context_similarity_check(text) if not emoji else emoji
    return emoji if emoji else text
  
  @staticmethod
  @jit(nopython=True)
  def cosine_similarity_numba(u:np.ndarray, v:np.ndarray):
    assert(u.shape[0] == v.shape[0])
    uv = 0
    uu = 0
    vv = 0
    for i in range(u.shape[0]):
        uv += u[i]*v[i]
        uu += u[i]*u[i]
        vv += v[i]*v[i]
    cos_theta = 0
    if uu!=0 and vv!=0:
        cos_theta = uv/np.sqrt(uu*vv)
    return cos_theta
  
