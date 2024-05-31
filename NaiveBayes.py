import re # Biblioteca de regex

rotten = []
fresh = []

common_word = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there",
    "their", "what", "so", "up", "out", "if", "about", "who", "get",
    "which", "go", "me", "i", "pron"
    ]

# Tabla de frecuencias (Bag of words)
def crear_tabla_frecuencias(corpus):
    frecuencias = {}
    for oracion in corpus:
        critica = oracion.lower()
        critica = re.sub(r'\W', ' ', critica)
        critica = re.sub(r'\s+', ' ', critica)
        tokens = critica.split(" ")
        for token in tokens:
            if token not in common_word:
                if token not in frecuencias.keys():
                    frecuencias[token] = 1
                else:
                    frecuencias[token] += 1
    return frecuencias

# Contar la cantidad total de palabras de todas las muestras de los arreglos
def contar_palabras(corpus):
    frecuenia = 0
    for oracion in corpus:
        frecuenia += len(oracion.split(" "))
    return frecuenia

# Cálculo utilizando laplace Smooting para evitar que se den probabilidades como 0.
def transformar_frecuencia_probabilidad_laplace(frecuencias, total):
    cpt_equivalente = {}
    n = 1
    k = len(frecuencias)
    for key,v in frecuencias.items():
        probabilidad  = (v + n) / (total + (n*k))
        cpt_equivalente[key] = probabilidad
    return cpt_equivalente

class Start():
    def __init__(self) -> None:
        total_oraciones = len(rotten) + len(fresh)

        # PROBABILIDADES TOTALES
        self.p_rotten = len(rotten) / total_oraciones
        self.p_fresh = len(fresh) / total_oraciones

        self.frecuencia_rotten = crear_tabla_frecuencias(rotten)
        self.frecuencia_fresh = crear_tabla_frecuencias(fresh)

        self.total_rotten = contar_palabras(rotten)
        self.total_fresh = contar_palabras(fresh)

        self.cpt_rotten_laplace = transformar_frecuencia_probabilidad_laplace(self.frecuencia_rotten, self.total_rotten)
        self.cpt_fresh_laplace = transformar_frecuencia_probabilidad_laplace(self.frecuencia_fresh, self.total_fresh)

# Método de la inferencia
def esFresco(system, critica):
    critica = critica.lower()
    critica = re.sub(r'\W', ' ', critica)
    critica = re.sub(r'\s+', ' ', critica)
    tokens = critica.split(" ")
    kf = len(system.frecuencia_fresh)
    kr = len(system.frecuencia_rotten)
    n = 1

    acumuladoRotten = 1.0
    acumuladoFresh = 1.0

    for token in tokens:
        if token not in system.cpt_fresh_laplace:
            acumuladoFresh *= (0 + n) / (system.total_fresh + (n*kf))
        else:
            acumuladoFresh *= system.cpt_fresh_laplace[token]
        
        if token not in system.cpt_rotten_laplace:
            acumuladoRotten *= (0 + n) / (system.total_rotten + (n*kr))
        else:
            acumuladoRotten *= system.cpt_rotten_laplace[token]

    resultadoFresco = (acumuladoFresh * system.p_fresh)
    resultadoPodrido = (acumuladoRotten * system.p_rotten)

    if resultadoFresco >= resultadoPodrido:
        return "Fresh"
    else:
        return "Rotten"

# INFERENCIA
# Rotten
frase = "For what it is and for whom it is intended, it's not a bad movie, just an indifferent one."
#fresh existe
frase2 = "A fantasy adventure that fuses Greek mythology to contemporary American places and values. Anyone around 15 (give or take a couple of years) will thrill to the visual spectacle"
# fresh no existe
frase3 = "Percy Jackson may not be ""Harry Potter good,"" but kids will really enjoy it and parents will be happy to have a moviethey can bring them to that's family-friendly."
# Rotten no existe
frase4 = "Bring on the David Fincher-helmed remake."
# P(ROTTEN | frase) =
# P(frase | ROTTEN) = P(palabra1 | Rotten) + P(palabra2 | Rotten) + P(palabra3 | Rotten) + ... + P(palabraN | Rotten)
# Frase sea rotten

if __name__ == '__main__':
    app = Start()
    print("Hello world")
    print(esFresco(app, frase))
    print(esFresco(app, frase2))
    print(esFresco(app, frase3))
    print(esFresco(app, frase4))