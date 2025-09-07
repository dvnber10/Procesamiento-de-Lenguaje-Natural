from nltk.tokenize import word_tokenize
import nltk

# librerias para lematización
from nltk.stem import WordNetLemmatizer

#mejor opción de lematizado


nltk.download('wordnet')
nltk.download('omw-1.4')

lematizar = WordNetLemmatizer()
def lematizar_texto(texto):
    tokens = word_tokenize(texto)
    lematizado = [lematizar.lemmatize(token) for token in tokens]
    return lematizado

def chat():
    print('chat: Hola, soy tu asistente virtual')
    while True:
        entrada = input("Escribe un texto para lematizar: ")
        if entrada.lower() == 'salir':
            print("Saliendo del chat.")
            break
        resultado = lematizar_texto(entrada)
        print("Chat:", resultado)

input_text = input("Escribe un texto para lematizar: ")
resultado = lematizar_texto(input_text)
print("Texto lematizado:", resultado)