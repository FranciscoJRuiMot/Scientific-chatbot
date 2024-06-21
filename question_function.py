#Function in order to E¡extract key words from a question in spanish

from deep_translator import GoogleTranslator
from nltk import word_tokenize
from nltk.corpus import stopwords

def keys_from_question():
    question = str(input())
    tokens = word_tokenize(question)
    stop_words = stopwords.words('spanish')
    words = [word for word in tokens if word.isalpha()]
    key_words = [key for key in words if not key in stop_words]
    #to do: se lanza una interfaz al usuario con estas key_worlds para que las seleccione
    return key_words