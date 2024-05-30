import re # Biblioteca de regex

rotten = [
    "What's really lacking in The Lightning Thief is a genuine sense of wonder, the same thing that brings viewers back to Hogwarts over and over again.",
    "It's more a list of ingredients than a movie-magic potion to enjoy from start to finish.",
    "Harry Potter knockoffs don't come more transparent and slapdash than this wannabe-franchise jumpstarter directed by Chris Columbus.",
    "Trifles, trivialities, frippery and froth. We've got plenty of words to describe things that don't matter. And now, we also have a film. Please Give.",
    "Real joys and sorrows must be bigger and deeper than this.",
    "The acting quality is strong, especially from the ever-reliable Catherine Keener as Kate, but it's almost impossible to care about her character's dilemmas.",
    "The film is more emotionally incisive than it initially appears to be, but equally it ties together a little too neatly when it already has such a concise running time.",
    "It was a big hit. I have never understood why.",
    ]
fresh = [
    "A fantasy adventure that fuses Greek mythology to contemporary American places and values. Anyone around 15 (give or take a couple of years) will thrill to the visual spectacle",
    "Uma Thurman as Medusa, the gorgon with a coiffure of writhing snakes and stone-inducing hypnotic gaze is one of the highlights of this bewitching fantas",
    "With a top-notch cast and dazzling special effects, this will tide the teens over until the next Harry Potter instalment",
    "With her new film, the poignant and funny Please Give, Holofcener is at the top of her game.",
    "Brutally honest about the way people behave, and often devastatingly funny in its observations.",
    "It recognizes that a film about unpleasant people need not be unpleasant itself as long as it remembers not to make them uninteresting as well.",
    "The film's premise yields a story that's insightful and engaging while touching on many other matters of love and money.",
    ]

total_oraciones = len(rotten) + len(fresh)
# PROBABILIDADES TOTALES
p_rotten = len(rotten) / total_oraciones
p_fresh = len(fresh) / total_oraciones

def contar_total(corpus):
    total = 0
    for oracion in corpus:
        critica = oracion.lower()
        critica = re.sub(r'\W', ' ', critica)
        critica = re.sub(r'\s+', ' ', critica)
        tokens = critica.split(" ")
        total += len(tokens)
    return total

cantidad_palabras_rotten = contar_total(rotten)
cantidad_palabras_fresh = contar_total(fresh)

# Tabla de frecuencias (Bag of words)
def crear_tabla_frecuencias(corpus):
    frecuencias = {}
    for oracion in corpus:
        critica = oracion.lower()
        critica = re.sub(r'\W', ' ', critica)
        critica = re.sub(r'\s+', ' ', critica)
        tokens = critica.split(" ")
        for token in tokens:
            if token not in frecuencias.keys():
                frecuencias[token] = 1
            else:
                frecuencias[token] += 1
    return frecuencias

def contar_palabras(corpus):
    frecuenia = 0
    for oracion in corpus:
        frecuenia += len(oracion.split(" "))
    return frecuenia

total_rotten = contar_palabras(rotten)
total_fresh = contar_palabras(fresh)
frecuencia_rotten = crear_tabla_frecuencias(rotten)
frecuencia_fresh = crear_tabla_frecuencias(fresh)


def transformar_frecuencia_probabilidad(frecuencias, total):
    cpt_equivalente = {}
    for k,v in frecuencias.items():
        probabilidad  = v / total
        cpt_equivalente[k] = probabilidad
    return cpt_equivalente

def transformar_frecuencia_probabilidad_laplace(frecuencias, total):
    cpt_equivalente = {}
    n = 1
    k = len(frecuencias)
    for key,v in frecuencias.items():
        probabilidad  = (v + n) / (total + (n*k))
        cpt_equivalente[key] = probabilidad
    return cpt_equivalente

# PROBABILIDAD DE PALABRAS POR CATEGORÍA
cpt_rotten = transformar_frecuencia_probabilidad(frecuencia_rotten, total_rotten)
cpt_fresh = transformar_frecuencia_probabilidad(frecuencia_fresh, total_fresh)

cpt_rotten_laplace = transformar_frecuencia_probabilidad_laplace(frecuencia_rotten, total_rotten)
cpt_fresh_laplace = transformar_frecuencia_probabilidad_laplace(frecuencia_fresh, total_fresh)

# INFERENCIA
# Rotten
frase = "For what it is and for whom it is intended, it's not a bad movie, just an indifferent one."
#fresh existe
frase2 = "A fantasy adventure that fuses Greek mythology to contemporary American places and values. Anyone around 15 (give or take a couple of years) will thrill to the visual spectacle"
# fresh no existe
frase3 = "Percy Jackson may not be ""Harry Potter good,"" but kids will really enjoy it and parents will be happy to have a moviethey can bring them to that's family-friendly."
# P(ROTTEN | frase) =
# P(frase | ROTTEN) = P(palabra1 | Rotten) + P(palabra2 | Rotten) + P(palabra3 | Rotten) + ... + P(palabraN | Rotten)
# Frase sea rotten

def esFresco(critica):
    resultado = 0
    critica = critica.lower()
    critica = re.sub(r'\W', ' ', critica)
    critica = re.sub(r'\s+', ' ', critica)
    tokens = critica.split(" ")
    kf = len(frecuencia_fresh)
    kr = len(frecuencia_rotten)
    n = 1

    acumuladoRotten = 1.0
    acumuladoFresh = 1.0

    for token in tokens:
        if token not in cpt_fresh_laplace:
            acumuladoFresh *= (0 + n) / (total_fresh + (n*kf))
        else:
            acumuladoFresh *= cpt_fresh_laplace[token]
        
        if token not in cpt_rotten_laplace:
            acumuladoRotten *= (0 + n) / (total_rotten + (n*kr))
        else:
            acumuladoRotten *= cpt_rotten_laplace[token]
        

    resultadoFresco = (acumuladoFresh * p_fresh)
    resultadoPodrido = (acumuladoRotten * p_rotten)

    if resultadoFresco >= resultadoPodrido:
        return "Fresh"
    else:
        return "Rotten"





if __name__ == '__main__':
    print("Hello world")
    print(esFresco(frase))
    print(esFresco(frase2))
    print(esFresco(frase3))
    # print(cpt_fresh)
    # print(cpt_rotten)
    # frecuenia_fresh = crear_tabla_frecuencias(fresh)
    # print(frecuenia_fresh)
    # print(frecuencia_rotten)
    # print(cpt_rotten)
