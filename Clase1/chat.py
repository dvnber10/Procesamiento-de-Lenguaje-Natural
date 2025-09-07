import nltk
from nltk.tokenize import word_tokenize
import spacy

nltk.download('punkt_tab')
pln = spacy.load("es_core_news_lg")

def lematizar_oracion(oracion):
    tokens = word_tokenize(oracion)
    lematizar_oracion = [token.lemma_ for token in pln(" ".join(tokens))]
    return lematizar_oracion

def lematizar_con_POS(texto):
    doc = pln(texto)
    return [(token.text, token.lemma_, token.pos_) for token in doc]

def tokenizar_oracion(oracion):
    return word_tokenize(oracion)

def chat():
    while True:
        entrada = input("Hola, ¿que quieres hacer?")
        if entrada.lower() == 'salir':
            print("Saliendo del chat.")
            break
        lematizar = lematizar_oracion(entrada)
        print("Lematización:", lematizar)
        
        if 'lematizar' in lematizar:
            entrada_chat = input("Escribe una oración para lematizar:" )
            lematizar_resultado = lematizar_oracion(entrada_chat)
            print("Oración lematizada:", lematizar_resultado)
        elif 'tokenizar' in lematizar:
            entrada_chat = input("Escribe una oración para tokenizar: ")
            tokenizar_resultado = tokenizar_oracion(entrada_chat)
            print("Oración tokenizada:", tokenizar_resultado)
        elif 'POS' in lematizar or 'analizar' in lematizar:
            entrada_chat = input("Escribe una oración para analizar: ")
            analizar_resultado = lematizar_con_POS(entrada_chat)
            print("Análisis de la oración:", analizar_resultado)
        else:
            print("No entiendo lo que quieres hacer, escoje entre lematizar o tokenizar.")

chat()
