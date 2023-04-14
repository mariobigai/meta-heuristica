import math
from lista1 import funcoes
from lista1 import plotagem
import numpy as np
from lista1 import AlgoritmoGenetico
from geneticalgorithm2 import plot_several_lines

#-------------------------------------------------------------
#Escolhe a função a ser otimizada, e define os limites avaliação
while(True):
    ex = input("Qual função será otimizada ? "
               "\n1 - Função de Schwefel com d = 2"
               "\n2 - Função Rastringin"
               "\n3 - Função Exponencial\n")

    if int(ex) == 1:
        ## Define os limites e cria o linspace
        x = np.arange(-500, 500.5, 0.5)
        y = np.arange(-500, 500.5, 0.5)
        XY =np.array([x,y])
        X = np.meshgrid(x, y)  # Retorna matrizes de cordenadas
        func = funcoes.func1   # fitness = custo
        nome_funcao = 'Schwefel'
        Z = func(X)  # Avalia a função em todos os pontos - Para plotagem (meshgrid)
        break
    elif int(ex) == 2:
        x = np.arange(-5, 5.05, 0.05)
        y = np.arange(-5, 5.05, 0.05)
        X = np.meshgrid(x, y)
        XY =np.array([x,y])# Retorna matrizes de cordenadas
        func = funcoes.func2 # fitness = custo
        nome_funcao = 'Rastringin'
        Z = func(X)  # Avalia a função em todos os pontos - Para plotagem (meshgrid)
        break
    elif int(ex) == 3:
        x = np.arange(-2, 2.05, 0.05)
        y = np.arange(-2, 2.05, 0.05)
        X = np.meshgrid(x, y)
        XY =np.array([x,y])# Retorna matrizes de cordenadas
        func = funcoes.func4 #Define fitness = 1/(1+custo)
        nome_funcao = 'Exponencial'
        Z = funcoes.func3(X)  # Avalia a função em todos os pontos - Para plotagem (meshgrid)
        break
    else: print("Escolha entre 1,2 e 3\n")

#label_y do relatório
if func == funcoes.func4:
    label_y = 'Função Maximizada'
else:
    label_y = 'Função Minimizada'

lista_solucoes = []
lista_fitness = []
lista_otimo = []
lista_melhores_solucoes = []
lista_melhores_fitness = []
lista_melhores_otimos = []
#--------------------------------------------------------------------
#Gera modelos definidos em AlgoritmoGenetico.py
modelos = AlgoritmoGenetico.gera_modelos(np.array([[x[0], x[-1]], [x[0], x[-1]]]), func)

#Laço principal - Percorre cada modelo
for modelo in modelos:

    #Verifica qual modelo está rodando e define modelo_nome
    if 'uniform' in str(modelo.crossover) and 'ranking' in str(modelo.selection):
        modelo_nome = 'RankingUniforme'
    if 'uniform' in str(modelo.crossover) and 'tournament' in str(modelo.selection):
        modelo_nome = 'TorneioUniforme'
    if 'arithmetic' in str(modelo.crossover) and 'ranking' in str(modelo.selection):
        modelo_nome = 'RankingAritimético'
    if 'arithmetic' in str(modelo.crossover) and 'tournament' in str(modelo.selection):
        modelo_nome = 'TorneioAritimético'

    #Define os parâmetros do relatório de evolução de fitness
    modelo.checked_reports.extend(
        [('report_avarage', np.mean), ('report_worst', np.max)]
    )
    #seta o melhor_fitness_geral inicial
    melhor_fitness_geral_modelo = math.inf

    #Lógica para pegarmos o modelo com melhor fintnesse fazer o relatório de evolução de fitness
    melhor_modelo = 0

    #lista para box-plot de numero de gerações
    lista_num_gen = []

    #Roda o modelo da iteração 10 vezes
    for i in range(10):
        modelo.run(no_plot=True) #roda a otimização

        num_geracoes = len(modelo.report)
        lista_num_gen.append(num_geracoes) #guarda numero de gerações do modelo - boxplot

        #verifica se é o melhor fitness
        fitness = modelo.result.score
        if  fitness < melhor_fitness_geral_modelo:
            melhor_fitness_geral_modelo = fitness
            melhor_modelo = modelo

        lista_solucoes.append(modelo.result.variable) #salva solução
        lista_fitness.append(fitness) #salva fitness
        if func == funcoes.func4:
            lista_otimo.append(funcoes.func3(modelo.result.variable)) #salva ótimo - maximização
        else:
            lista_otimo.append(func(modelo.result.variable))          #salva ótimo - minimização

    lista_melhores_fitness.append(melhor_fitness_geral_modelo)  # Salva melhor fitness das 10 iterações
    lista_melhores_solucoes.append(melhor_modelo.result.variable) #Salva a melhor solução das 10 iterações
    if func == funcoes.func4:
        lista_melhores_otimos.append(funcoes.func3(melhor_modelo.result.variable)) #Salva melhor ótimo - maximização
    else:
        lista_melhores_otimos.append(func(melhor_modelo.result.variable)) #Salva melhor ótimo - minimização

    names = [name for name, _ in melhor_modelo.checked_reports[::-1]] #separa as variáveis do checked_reports
    lines = [getattr(melhor_modelo, name) for name in names]          #gera os fitness temporais
    pior_fitness_temporal = lines[0]
    medio_fitness_temporal = lines[1]
    melhor_fitness_temporal = lines[2]

    valor_maximo = max([max(lista) for lista in lines]) #Maior fitness de todos
    valor_minimo = min([min(lista) for lista in lines]) #Menor fitness de todos

    pior_fitness_temporal_nomalizado = [1/(1+((fit-valor_minimo)/(valor_maximo-valor_minimo))) for fit in pior_fitness_temporal]
    medio_fitness_temporal_nomalizado = [1/(1+(fit - valor_minimo) / (valor_maximo - valor_minimo)) for fit in medio_fitness_temporal]
    melhor_fitness_temporal_nomalizado = [1/(1+(fit - valor_minimo) / (valor_maximo - valor_minimo)) for fit in melhor_fitness_temporal]

    num_geracoes_temporal = list(np.arange(1,num_geracoes+1,1))

    # -------------------------------------------------------------------------------------------------------------------
    #Save intermediário: Salva número de gerações de cada modelo (Melhor das 10 iterações)
    # Salva a quantidade de gerações de cada modelo para cada função em um TXT
    np.savetxt(f'./ListaNumGerações{modelo_nome}{nome_funcao}.txt', lista_num_gen, fmt='%d')
    print('\n', lista_num_gen)

    #-------------------------------------------------------------------------------------------------------------------
    #Plotagens itermediárias: Fitness temporal de cada modelo (Melhor das 10 iterações) e Box-Plot modelo (melhor das 10 iterações)
    plotagem.plotFitnessTemporal(f'{modelo_nome}',num_geracoes_temporal, pior_fitness_temporal_nomalizado, medio_fitness_temporal_nomalizado, melhor_fitness_temporal_nomalizado)
    plotagem.plota_boxplot(lista_num_gen, modelo_nome, nome_funcao)  # Plota e salva o Boxplot para cada modelo da função

#----------------------------------------------------------------------------------------------------------------------
#Saves Finais: Lista de soluções, fitness e ótimos, melhores soluções melhores fitness e melhores ótimos
#Salva todas as soluções encontradas
np.savetxt(f'./ListaSolus{nome_funcao}.txt', lista_solucoes, fmt='%s')
print('\n', lista_solucoes)

#Salva as melhores soluções encontradas
np.savetxt(f'./ListaMelhoresSolus{nome_funcao}.txt', lista_melhores_solucoes, fmt='%s')
print('\n', lista_melhores_solucoes)

#Salva todos os fitness encontrados
np.savetxt(f'./ListaFit{nome_funcao}.txt', lista_fitness, fmt='%f')
print('\n', lista_fitness)

#Salva os melhores fitness encontrados
np.savetxt(f'./ListaMelhoresFit{nome_funcao}.txt', lista_melhores_fitness, fmt='%f')
print('\n', lista_melhores_fitness)

#Salva os ótimos encontrados
np.savetxt(f'./ListaOtimo{nome_funcao}.txt', lista_otimo, fmt='%f')
print('\n', lista_otimo)

#Salva os ótimos encontrados
np.savetxt(f'./ListaMelhoresOtimo{nome_funcao}.txt', lista_melhores_otimos, fmt='%f')
print('\n', lista_melhores_otimos)
#-------------------------------------------------------------
#Plotagem final:

melhor_solucao_de_todas = lista_melhores_solucoes[lista_melhores_fitness.index(min(lista_melhores_fitness))]

if func == funcoes.func4:
    # Plota o gráfico 3D com o a solução destacada - maximização
    plotagem.plota_3D(X[0], X[1], Z, funcoes.func3, lista_solucoes, lista_melhores_solucoes, melhor_solucao_de_todas)
else:
    #Plota o gráfico 3D com o a solução destacada - minimização
    plotagem.plota_3D(X[0], X[1], Z, func, lista_solucoes, lista_melhores_solucoes, melhor_solucao_de_todas)