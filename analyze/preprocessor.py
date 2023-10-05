import re
import ssl
import string

import nltk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
nltk.download('punkt')  
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer



def remove_punctuation(s):
    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    return s.translate(translator)


def remove_stop_words(input_str):
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(input_str)
    result = [i for i in tokens if i not in stop_words]
    joined_result = ' '.join(result)
    return joined_result


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def lemmatizing(input_str):
    lemmatizer = WordNetLemmatizer()
    input_str = word_tokenize(input_str)
    result = [lemmatizer.lemmatize(i, get_wordnet_pos(i)) for i in input_str]
    return ' '.join(result)


def remove_unusual_char(input_str):
    return re.sub('[^A-Za-z0-9 ]+', '', input_str)


def pre_process(data):
    processing_data = data.map(lambda s: s.lower())
    processing_data = processing_data.map(lambda s: re.sub(r'\d+', '', s))
    processing_data = processing_data.map(lambda s: remove_punctuation(s))
    processing_data = processing_data.map(lambda s: s.strip())
    processing_data = processing_data.map(lambda s: ' '.join(s.split()))
    processing_data = processing_data.map(lambda s: remove_stop_words(s))
    processing_data = processing_data.map(lambda s: remove_unusual_char(s))
    processing_data = processing_data.map(lambda s: lemmatizing(s))
    return processing_data

