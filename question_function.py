#Function in order to E¡extract key words from a question in spanish

from deep_translator import GoogleTranslator
from nltk import word_tokenize
from nltk.corpus import stopwords

def keys_from_question(question):
    translator = GoogleTranslator(source = 'es', target = 'en')
    tokens = word_tokenize(translator.translate(question))
    stop_words = stopwords.words('english')
    words = [word for word in tokens if word.isalpha()]
    key_words = [key for key in words if not key in stop_words]
    return key_words