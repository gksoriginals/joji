# Joji 
Joji convert a text to corresponding emoji if emoji is available

## How it Works ?
```
1. There is a json file with emoji names as keys and corresponding unicode of emojis as values.
2. There is a method that check if the input word is in the key space of the json. If yes then will return corresponding value.
3. There is a method that do similarity matching of word against the keys in json and return the emoji unicode corresponding to the key with maximum similarity value.
4. There is a threshold to avoid False Positives.
5. If both checking and matching don't return anything, just return the word - means there is no emoji for that word. 
```

## Libraries used
- [Spacy](https://spacy.io)
## How to configure 
```
python setup.py install 
```

## Install

Joji is now available in pip

```
pip install joji
```

## How to Run 

```python
>> from joji.jojify import Jojify
>> print(Jojify.predict("dracula"))
('🧛', 'U+1F9DB', 0.5509367532053601)
>> print(Jojify.predict("ganja"))
('🌿', 'U+1F33F', 0.2860632682239092)
>> print(Jojify.predict("ironman"))
('🦸', 'U+1F9B8', 0.40435058484084363)
>> print(Jojify.predict("good night"))
('👌🌃', ['U+1F44C', 'U+1F303'], 0.7178929764409834)
```

## How to Test 
```
pytest tests
```

## Future work
1. Maybe add [vaaku2vec](https://github.com/adamshamsudeen/Vaaku2Vec) and create malayalam text to emoji  
