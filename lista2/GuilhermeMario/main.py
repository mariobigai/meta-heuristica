# arquivo principal
import math
import numpy as np

# lendo arquivos e extraindo os pontos
def carrega_cidades(nome):
    nome_arquivo = nome
    cidades = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            index, x, y = int(linha.split()[0]), float(linha.split()[1]), float(linha.split()[2])
            cidades.append((index, x, y))
    return cidades
# calcula distância entre 2 cidades
def calcula_distancia(cidade1, cidade2):
    return math.sqrt((cidade1[1] - cidade2[1])**2 + (cidade1[2] - cidade2[2])**2)

# inicializa matriz custo - informação heurística
def init_matriz_custo(num_cidades, cidades):
    matriz_custo = []
    for i in range(num_cidades):
        linha = []
        for j in range(num_cidades):
            try:
                linha.append(1/calcula_distancia(cidades[i], cidades[j]))
            except ZeroDivisionError:
                linha.append((0))

        matriz_custo.append(linha)
    return np.array(matriz_custo)

# Matriz de ferômonios com valor inicial igual em todos os caminhos
def init_matriz_feromonios(num_cidades):
    A = np.ones((num_cidades, num_cidades))
    return (A - np.identity(num_cidades))*10e-6

def aco(cidades, n_iteracoes, alpha, beta, taxa_evaporacao, Q):
    # Inicializa
    num_cidades = len(cidades)
    num_formigas = num_cidades
    matriz_feromonios = init_matriz_feromonios(num_cidades)
    melhor_caminho = None
    tamanho_melhor_caminho = np.inf

    # Variáveis para fitness temporal
    fitness_melhor_temp = []
    fitness_medio_temp = []
    fitness_pior_temp = []

    #Critério de parada
    iteracao_sem_melhoria = 0

    #laço principal
    for iteracao in range(n_iteracoes):
        caminhos = []
        tamanho_caminhos = []

        # laço de construção dos caminhos
        for formiga in range(num_formigas):
            visitados = [False]*num_cidades #lista de cidades visitadas
            cidade_atual = np.random.randint(num_cidades)
            visitados[cidade_atual] = True
            caminho = [cidade_atual]
            tamanho_caminho = 0

            # laço das cidades-tabus e escolha da próxima cidade e definição do caminho
            while False in visitados:
                n_visitados = np.where(np.logical_not(visitados))[0] #Cria uma lista ordenada das cidades que não visitadas
                probabilidades = np.zeros(len(n_visitados))

                for i, cidade_n_visitada in enumerate(n_visitados):
                    probabilidades[i] = pow(matriz_feromonios[cidade_atual, cidade_n_visitada],alpha) * pow(matriz_custo[cidade_atual, cidade_n_visitada],beta)

                probabilidades /= sum(probabilidades)
                probabilidades = np.nan_to_num(probabilidades) #substitui NaN por 0
                #print(sum(probabilidades))
                try:
                    proxima_cidade = np.random.choice(n_visitados, p=probabilidades)
                except ValueError:
                    proxima_cidade = np.random.choice(n_visitados)
                caminho.append(proxima_cidade)
                tamanho_caminho += calcula_distancia(cidades[cidade_atual], cidades[proxima_cidade])
                visitados[proxima_cidade] = True
                cidade_atual = proxima_cidade

            # Calcula o tamanho final do caminho e salva na o caminho na lista
            tamanho_caminho += calcula_distancia(cidades[cidade_atual], cidades[caminho[0]]) #Considera o circuito fechado
            caminhos.append(caminho)
            tamanho_caminhos.append(tamanho_caminho)



            #salva melhor caminho e seu tamanho
            if tamanho_caminho < tamanho_melhor_caminho:
                melhor_caminho = caminho
                tamanho_melhor_caminho = tamanho_caminho
            else:
                iteracao_sem_melhoria += 1

            # Atualiza listas para fitness temporal
            fitness_melhor_temp.append(tamanho_melhor_caminho)
            fitness_medio_temp.append(np.average(tamanho_caminhos))
            fitness_pior_temp.append(max(tamanho_caminhos))

            #Atualização dos feromônios
            for caminho, tamanho_caminho in zip(caminhos, tamanho_caminhos):
                for i in range(num_cidades-1):
                    matriz_feromonios[caminho[i], caminho[i+1]] *= (1-taxa_evaporacao)
                    matriz_feromonios[caminho[i], caminho[i+1]] += Q / tamanho_caminho
                matriz_feromonios[caminho[-1], caminho[0]] *= (1 - taxa_evaporacao)
                matriz_feromonios[caminho[-1], caminho[0]] += Q / tamanho_caminho

            if iteracao_sem_melhoria == 10:
                break

    return melhor_caminho, tamanho_melhor_caminho, fitness_melhor_temp, fitness_medio_temp, fitness_pior_temp, iteracao

cidades = carrega_cidades('djibout.txt')
num_cidades = len(cidades)
matriz_custo = init_matriz_custo(num_cidades, cidades)

melhor_caminho, tamanho_melhor_caminho, fitness_melhor_temp, fitness_medio_temp, fitness_pior_temp, iteracao = aco(cidades, 25, 1.0, 5.0, 0.5, 100)
print(melhor_caminho, tamanho_melhor_caminho)
print('\n')
print(fitness_melhor_temp)
print('\n')
print(fitness_medio_temp)
print('\n')
print(fitness_pior_temp)
print('\n')
print(iteracao)