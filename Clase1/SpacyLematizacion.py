import spacy
# importacion del tokenizado
from nltk.tokenize import word_tokenize
import nltk

#cargar modelo en idioma español
pln = spacy.load("es_core_news_sm")

def lematizar_oracion(oracion):
    tokens = word_tokenize(oracion)
    lematizar_oracion = [token.lemma_ for token in pln(" ".join(tokens))]
    return lematizar_oracion

def chat():
    while True:
        entrada = input("Escribe una oración para lematizar (o 'salir' para terminar): ")
        if entrada.lower() == 'salir':
            print("Saliendo del chat.")
            break
        lematizado = lematizar_oracion(entrada)
        print("Oración lematizada:", lematizado)

chat()
    
    