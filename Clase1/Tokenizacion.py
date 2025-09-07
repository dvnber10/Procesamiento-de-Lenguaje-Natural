#librerias necesarias
from nltk.tokenize import word_tokenize
import nltk

# ddescarga del paquete
nltk.download('punkt_tab')

chat = 'Hola, preguntame algo'

def chat_texto(chat):
    tokens = word_tokenize(chat)
    if 'hola' in tokens:
        print('Hola, ¿en qué puedo ayudarte?')
    else:
        print('Saludame primero')

while True:
    
    print('chat_texto:', chat)
    response = input('Escribe tu mensaje: ')
    if response == 'salir':
        break
    print('Respuesta del chat:', chat_texto(response))
    