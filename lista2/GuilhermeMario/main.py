# arquivo principal
import math

# lendo arquivos e extraindo os pontos
def carrega_cidades(nome):
    nome_arquivo = nome
    cidades = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            index, x, y = int(linha.split()[0]), float(linha.split()[1]), float(linha.split()[2])
            cidades.append((index, x, y))
    return cidades

def calcula_distancia(cidade1, cidade2):
    return math.sqrt((cidade1[1] - cidade2[1])**2 + (cidade1[2] - cidade2[2])**2)

cidades = carrega_cidades('Luxemburgo.txt')
print(cidades[0:5])
print(calcula_distancia(cidades[0], cidades[2]))