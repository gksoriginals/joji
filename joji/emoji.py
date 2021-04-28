import os
import json
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
  "data/emoji_dict.p"
)
infile = open(emoji_dict_path, 'rb')
emoji_dict = pickle.load(infile)
infile.close()

class Jojify(object):
  """
  class containing methods to map text to emoji
  """  
  emoji_dict = emoji_dict
  
  @classmethod
  def _simple_check(cls, text):
    if text in cls.emoji_dict:
      return (
        cls.emoji_dict.get(text).get("emoji"),
        cls.emoji_dict.get(text).get("unicode"),
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
        max_emoji = cls.emoji_dict.get(emoji_name).get("emoji")
        max_unicode = cls.emoji_dict.get(emoji_name).get("unicode")
        max_score = score
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
  
