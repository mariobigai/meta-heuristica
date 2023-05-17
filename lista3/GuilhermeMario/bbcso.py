# Desenvolvimento do BBCSO

"""
Código inspirado em: https://github.com/CacaAlves00/BBCSO
"""
import operator
from operator import xor
import math
import random
import numpy as np
from enum import Enum

def roulette(values, fitness_values):
    max = sum([fit for fit in fitness_values])
    if max == 0.0:
        return values[np.random.choice(np.array(values))]

    selection_probs = [fit/max for fit in fitness_values]

    return values[np.random.choice(len(values), p=selection_probs)]

#Classe para enumerar e classificar os gatos
class Tipo_de_Gato(Enum):
    SEEKING = 1
    TRACING = 2

class Gato:
    def __init__(self, tipo, tamanho_dimensao, parametros, funcao_fitness):
        self.tipo = tipo
        self.tamanho = tamanho_dimensao
        self.posicoes = self.init_posicoes(tamanho_dimensao)
        self.velocidade = np.zeros(tamanho_dimensao)
        self.paremetros = parametros
        self.funcao_fitness = funcao_fitness

    def init_posicoes(self, tamanho_dimensoes):
        A = np.zeros(tamanho_dimensoes)
        for index in range(0, len(A)):
            A[index] = random.randrange(0,2)
        return A

    def avalia_fitness(self):
        return self.funcao_fitness(self.posicoes)

    # dunder method para comparar o fitness entre 2 gatos
    def __lt__(self, outro):
        return self.avalia_fitness() < outro.avalia_fitness()

    def seleciona_gato(self, gatos):
        valores_fit_gatos = ([self.funcao_fitness(gato.posicoes) for gato in gatos])
        return roulette(gatos, valores_fit_gatos)

    def copia_gatos(self):
        copia = Gato(
            tipo=self.tipo,
            tamanho_dimensao = self.tamanho,
            parametros= self.paremetros,
            funcao_fitness=self.funcao_fitness
            )
        copia.posicoes = np.copy(self.posicoes)
        copia.velocidade = np.copy(self.velocidade)

        return copia

    def mutacao(self):
        #posições que serão mutadas
        for _ in range(self.paremetros['CDC']):
            faz_mutacao = random.uniform(0,1) < self.paremetros['PMO'] #Probabilidade de mutação
            if not faz_mutacao:
                return
            bit_aleotorio = random.randrange(0, self.tamanho)
            valor_atual = self.posicoes[bit_aleotorio]
            #Faz a mutação: 0->1 ou 1->)
            self.posicoes[bit_aleotorio] = 0 if valor_atual == 1 else 1

    def copia_e_muta(self):
        # Cria SPM clones de cada gato
        clones = [self.copia_gatos() for _ in range(0, self.paremetros['SPM'])]

        for clone in clones:
            clone.mutacao()

        return clones

    def atualiza_velocidade(self, dimensao, gbest):
        r1 = random.randrange(0,2) #Gera 0 ou 1
        velocidade_valor = int(self.velocidade[dimensao])

        self.velocidade[dimensao] = xor(r1, velocidade_valor) and gbest.posicoes[dimensao] or self.posicoes[dimensao]

    def atualiza_posicao(self, dimensao):
        self.posicoes[dimensao] = self.posicoes[dimensao] or self.velocidade[dimensao]

    def movimentacao_seeking(self):
        gatos = self.copia_e_muta()
        gatos.append(self)

        return self.seleciona_gato(gatos)

    def movimentacao_tracing(self, gbest):
        for dimensao in range(0, self.tamanho):
            self.atualiza_posicao(dimensao)
            self.atualiza_velocidade(dimensao, gbest)
        return self

    def movimenta(self, gbest):
        if self.tipo == Tipo_de_Gato.SEEKING:
            return self.movimentacao_seeking()
        elif self.tipo == Tipo_de_Gato.TRACING:
            return self.movimentacao_tracing(gbest)
        else:
            raise Exception('Tipo invalido para gato')

class BBCSO:
    def __init__(self, n_gatos, dimensoes, parametros, funcao_fitness):
        self.n_gatos = n_gatos
        self.parametros = parametros
        self.gatos = []
        self.init_gatos(dimensoes, funcao_fitness)
        self.gbest = self.gatos[0]
        self.gbest_fitness = 0.0

    def init_gatos(self, dimensoes, funcao_fitness):
        for _ in range(0, self.n_gatos):
            self.gatos.append(Gato(
                tipo = None,
                tamanho_dimensao = dimensoes,
                parametros = self.parametros,
                funcao_fitness = funcao_fitness
            ))

    def define_gbest(self):
        lista_fitness = [gato.avalia_fitness() for gato in self.gatos]
        for gato in self.gatos:
            fitness_atual = gato.avalia_fitness()

            if (fitness_atual > self.gbest_fitness):
                self.gbest = gato
                self.gbest_fitness = fitness_atual

        return self.gbest_fitness, np.mean(lista_fitness), np.min(lista_fitness)

    def seleciona_tracing_seeking(self):
        #Ordenando por fitness crescente
        self.gatos.sort(reverse=True)

        n_gatos_tracing = math.floor(self.parametros['MR']*self.n_gatos)

        #Separa os gatos em TRACING e SEEKING de acordo com o MR - Porcentagem de gatos fazendo Tracing
        for gato_index in range(0, n_gatos_tracing):
            self.gatos[gato_index].tipo = Tipo_de_Gato.TRACING
        for gato_index in range(n_gatos_tracing, self.n_gatos):
            self.gatos[gato_index].tipo = Tipo_de_Gato.SEEKING

    def move_gatos(self):
        for gato_index in range(0, self.n_gatos):
            self.gatos[gato_index] = self.gatos[gato_index].movimenta(self.gbest)

    def run(self, dimensoes):
        iteracoes = 0
        melhor_fitness = []
        medio_fitness = []
        pior_fitness = []
        self.define_gbest()
        while (self.gbest_fitness != sum(dimensoes*[1.])):
            melhor_atual, medio_atual, pior_atual = self.define_gbest()
            melhor_fitness.append(melhor_atual)
            medio_fitness.append(medio_atual)
            pior_fitness.append(pior_atual)
            self.seleciona_tracing_seeking()
            self.move_gatos()
            iteracoes += 1
        melhor_atual, medio_atual, pior_atual = self.define_gbest()
        melhor_fitness.append(melhor_atual)
        medio_fitness.append(medio_atual)
        pior_fitness.append(pior_atual)
        return iteracoes, melhor_fitness, medio_fitness, pior_fitness

        self.define_gbest()
        return self.gbest, self.gbest_fitness, iteracoes