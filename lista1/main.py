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
        func = funcoes.func1
        nome_funcao = 'Schwefel'
        break
    elif int(ex) == 2:
        x = np.arange(-5, 5.05, 0.05)
        y = np.arange(-5, 5.05, 0.05)
        X = np.meshgrid(x, y)
        XY =np.array([x,y])# Retorna matrizes de cordenadas
        func = funcoes.func2
        nome_funcao = 'Rastringin'
        break
    elif int(ex) == 3:
        x = np.arange(-2, 2.05, 0.05)
        y = np.arange(-2, 2.05, 0.05)
        X = np.meshgrid(x, y)
        XY =np.array([x,y])# Retorna matrizes de cordenadas
        func = funcoes.func3
        nome_funcao = 'Exponencial'
        break
    else: print("Escolha entre 1,2 e 3\n")
Z = func(X)  #  Avalia a função em todos os pontos - Para plotagem (meshgrid)

#label_y do relatório
if func == funcoes.func3:
    label_y = 'Função Mininzada'
else:
    label_y = 'Função Maximizada'

lista_melhores_fitness = []
lista_melhores_solucoes = []
lista_otimo_encontrado = []
#--------------------------------------------------------------------
modelos = AlgoritmoGenetico.gera_modelos(np.array([[x[0], x[-1]], [x[0], x[-1]]]), func)
for modelo in modelos:

    #Checkar qual modelo estamos e definir modelo_nome
    if 'uniform' in str(modelo.crossover) and 'roulette' in str(modelo.selection):
        modelo_nome = 'RoletaUniforme'
    if 'uniform' in str(modelo.crossover) and 'tournament' in str(modelo.selection):
        modelo_nome = 'TorneioUniforme'
    if 'arithmetic' in str(modelo.crossover) and 'roulette' in str(modelo.selection):
        modelo_nome = 'RoletaAritimético'
    if 'arithmetic' in str(modelo.crossover) and 'tournament' in str(modelo.selection):
        modelo_nome = 'TorneioAritimético'

    #Define os parâmetros do relatório de evolução de fitness
    modelo.checked_reports.extend(
        [('report_avarage', np.mean), ('report_worst', np.max)]
    )

    #Lógica para pegarmos o modelo com melhor fintnesse fazer o relatório de evolução de fitness
    melhor_modelo = 0
    melhor_fitness_geral_modelo = math.inf

    #lista para box-plot de numero de gerações
    lista_num_gen = []

    for i in range(10):
        modelo.run(no_plot=True) #roda a otimização
        num_geracoes = len(modelo.report)
        lista_num_gen.append(num_geracoes) #guarda numero de gerações do modelo

        #verifica se é o melhor fitness entre os 10
        melhor_fitness = modelo.result.score
        if melhor_fitness < melhor_fitness_geral_modelo:
            melhor_fitness_geral_modelo = melhor_fitness
            melhor_modelo = modelo

    names = [name for name, _ in melhor_modelo.checked_reports[::-1]]
    plot_several_lines(
        lines=[getattr(melhor_modelo, name) for name in names],
        colors=('green', 'red', 'blue'),
        labels=['pior fitness', 'fitness medio', 'melhor fitness'],
        linewidths=(1, 1.5, 1, 2),
        xlabel='Gerações',
        ylabel=label_y,
        title=f'{modelo_nome} {nome_funcao}',
        save_as=f'./{modelo_nome}{nome_funcao}'
    )

    lista_melhores_fitness.append(melhor_fitness_geral_modelo) #Armazena melhor fitness do modelo
    lista_melhores_solucoes.append(melhor_modelo.result.variable)
    lista_otimo_encontrado.append(func(melhor_modelo.result.variable)) #Avalia a melhor solução na função e armazena na lista
#-------------------------------------------------------------
#Plotagens para relatório

print(lista_otimo_encontrado)
print(min(lista_otimo_encontrado))

if func == funcoes.func3:
    plotagem.plota_3D(X[0], X[1], Z) #Plota o gráfico
else:
    indice_melhor_solucao_de_todas = lista_otimo_encontrado.index(min(lista_otimo_encontrado))
    plotagem.plota_3D(X[0], X[1], Z, [lista_melhores_solucoes[indice_melhor_solucao_de_todas][0],
                                      lista_melhores_solucoes[indice_melhor_solucao_de_todas][1],
                                      min(lista_otimo_encontrado)]) #Plota o gráfico

