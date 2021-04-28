import os
import emoji
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

  @classmethod
  def _similarity_match_1(cls, word1, word2):
    word1 = nlp(word1)
    return cls.cosine_similarity_numba(word1.vector, word2.vector)

  @staticmethod
  def generate_unicode(emoj):
    return f'U+{ord(emoj):X}' if len(emoj) == 1 else None
  
  @staticmethod
  def _simple_check(text, emoji_dict):
    emoji_data, score = None, 0.0
    if text in emoji_dict:
      score = 1.0
      emoji_data = emoji_dict.get(text)
    return emoji_data, score
  
  @staticmethod
  def _similarity_match(word1, nlpfied2):
    word1 = nlp(word1) 
    return word1.similarity(nlpfied2)

  @staticmethod
  def get_vector(emoji_data):
    return emoji_data.get("vector")
    
  @classmethod  
  def _context_similarity_check(cls, text, emoji_dict):
    max_score = 0 # set threshold value instead
    max_emoji_data = None
    for emoji_name in emoji_dict:
      emoji_data = emoji_dict.get(emoji_name)
      vector = cls.get_vector(emoji_data)
      score = cls._similarity_match(text, vector)
      if score > max_score:
        max_score = score
        max_emoji_data = emoji_data
    return max_emoji_data, max_score

  @staticmethod
  def get_short_name(emoji_data):
    return emoji_data.get("short_name")

  @classmethod
  def get_emoji_and_unicode(cls, emoji_data):
    short_name = cls.get_short_name(emoji_data)
    max_emoji = emoji.emojize(short_name)
    max_unicode = cls.generate_unicode(max_emoji)
    return max_emoji, max_unicode

  @staticmethod
  def preprocess(text):
    text = text.lower()
    return text

  @classmethod
  def predict(cls, text):
    text = cls.preprocess(text)
    emoji_data, score = cls._simple_check(text, cls.emoji_dict)
    if not emoji_data:
      emoji_data, score = cls._context_similarity_check(text, cls.emoji_dict)
    max_emoji, max_unicode = cls.get_emoji_and_unicode(emoji_data)
    return (max_emoji, max_unicode, score) if score else text
  
  
