ALFABETO = ("a", "b", "c")
ESTADO_INICIAL = "qPar"
ESTADO_FINAL = "qImpar"
ESTADO_ERRO = "qErro"

TABELA_TRANSICOES = {
    "qPar": {
        "a": "qPar", "b": "qPar", "c": "qImpar",
        "d": "qErro", "e": "qErro", "f": "qErro", "g": "qErro",
        "h": "qErro", "i": "qErro", "j": "qErro", "k": "qErro",
        "l": "qErro", "m": "qErro", "n": "qErro", "o": "qErro",
        "p": "qErro", "q": "qErro", "r": "qErro", "s": "qErro",
        "t": "qErro", "u": "qErro", "v": "qErro", "w": "qErro",
        "x": "qErro", "y": "qErro", "z": "qErro",
    },
    "qImpar": {
        "a": "qImpar", "b": "qImpar", "c": "qPar",
        "d": "qErro", "e": "qErro", "f": "qErro", "g": "qErro",
        "h": "qErro", "i": "qErro", "j": "qErro", "k": "qErro",
        "l": "qErro", "m": "qErro", "n": "qErro", "o": "qErro",
        "p": "qErro", "q": "qErro", "r": "qErro", "s": "qErro",
        "t": "qErro", "u": "qErro", "v": "qErro", "w": "qErro",
        "x": "qErro", "y": "qErro", "z": "qErro",
    },
    "qErro": {
        "a": "qErro", "b": "qErro", "c": "qErro",
        "d": "qErro", "e": "qErro", "f": "qErro", "g": "qErro",
        "h": "qErro", "i": "qErro", "j": "qErro", "k": "qErro",
        "l": "qErro", "m": "qErro", "n": "qErro", "o": "qErro",
        "p": "qErro", "q": "qErro", "r": "qErro", "s": "qErro",
        "t": "qErro", "u": "qErro", "v": "qErro", "w": "qErro",
        "x": "qErro", "y": "qErro", "z": "qErro",
    },
}


def eh_letra_minuscula(simbolo: str) -> bool:
    return len(simbolo) == 1 and "a" <= simbolo <= "z"


def analisar(palavra: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Retorna o estado atingido e o percurso de uma palavra filtrada de a a z."""
    estado = ESTADO_INICIAL
    percurso = []
    for simbolo in palavra:
        destino = TABELA_TRANSICOES[estado][simbolo]
        percurso.append((estado, simbolo, destino))
        estado = destino
    return estado, percurso
