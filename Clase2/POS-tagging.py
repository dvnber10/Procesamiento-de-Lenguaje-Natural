import spacy

pln = spacy.load("es_core_news_lg")

lematizado= []

def lematizar_con_POS(texto):
    doc = pln(texto)
    return [(token.text,token.lemma_, token.pos_) for token in doc]

lematizado = lematizar_con_POS("Hola mundo")
print(lematizado)