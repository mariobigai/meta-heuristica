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

lista_melhores_fitness = []
lista_melhores_solucoes = []
lista_otimo_encontrado = []
#--------------------------------------------------------------------
modelos = AlgoritmoGenetico.gera_modelos(np.array([[x[0], x[-1]], [x[0], x[-1]]]), func)

#Laço principal
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
    melhor_fitness_geral_modelo = -math.inf

    #Lógica para pegarmos o modelo com melhor fintnesse fazer o relatório de evolução de fitness
    melhor_modelo = 0

    #lista para box-plot de numero de gerações
    lista_num_gen = []

    #Roda o modelo 10 vezes e salva o melhor resultado
    for i in range(10):
        modelo.run(no_plot=True) #roda a otimização

        num_geracoes = len(modelo.report)
        lista_num_gen.append(num_geracoes) #guarda numero de gerações do modelo - boxplot

        #verifica se é o melhor fitness
        melhor_fitness = modelo.result.score
        if func == funcoes.func4:
            if melhor_fitness > melhor_fitness_geral_modelo:
                melhor_fitness_geral_modelo = melhor_fitness
                melhor_modelo = modelo
        else:
            if melhor_fitness < melhor_fitness_geral_modelo:
                melhor_fitness_geral_modelo = melhor_fitness
                melhor_modelo = modelo

    names = [name for name, _ in melhor_modelo.checked_reports[::-1]] #separa as variáveis do checked_reports
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

    plotagem.plota_boxplot(lista_num_gen, modelo_nome,
                           nome_funcao)  # Plota e salva o Boxplot para cada modelo da função

    print('\n', lista_num_gen, '\n')
    # Salva a quantidade de gerações de cada modelo para cada função em um TXT
    np.savetxt(f'./ListaNumGerações{modelo_nome}{nome_funcao}.txt', lista_num_gen, fmt='%d')

#Salva as melhores soluções encontradas dos modelos
np.savetxt(f'./ListaMelhoresSolus{nome_funcao}.txt', lista_melhores_solucoes, fmt='%s')

#Salva os melhores fitness encontradas dos modelos
np.savetxt(f'./ListaMelhoresFit{nome_funcao}.txt', lista_melhores_fitness, fmt='%f')
#-------------------------------------------------------------
#Plotagens para relatório
print(lista_otimo_encontrado)
print(min(lista_otimo_encontrado))
print(lista_melhores_solucoes)

if func == funcoes.func4:
    indice_melhor_solucao_de_todas = lista_otimo_encontrado.index(min(lista_otimo_encontrado))
    # Plota o gráfico 3D com o a solução destacada
    plotagem.plota_3D(X[0], X[1], Z, [lista_melhores_solucoes[indice_melhor_solucao_de_todas][0],
                                      lista_melhores_solucoes[indice_melhor_solucao_de_todas][1],
                                      funcoes.func3(lista_melhores_solucoes[indice_melhor_solucao_de_todas])])
else:
    indice_melhor_solucao_de_todas = lista_otimo_encontrado.index(min(lista_otimo_encontrado))
    #Plota o gráfico 3D com o a solução destacada
    plotagem.plota_3D(X[0], X[1], Z, [lista_melhores_solucoes[indice_melhor_solucao_de_todas][0],
                                      lista_melhores_solucoes[indice_melhor_solucao_de_todas][1],
                                      min(lista_otimo_encontrado)])

