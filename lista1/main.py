from lista1 import funcoes
from lista1 import plotagem
import numpy as np
from lista1 import AlgoritmoGenetico

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
        break
    elif int(ex) == 2:
        x = np.arange(-5, 5.05, 0.05)
        y = np.arange(-5, 5.05, 0.05)
        X = np.meshgrid(x, y)
        XY =np.array([x,y])# Retorna matrizes de cordenadas
        func = funcoes.func2
        break
    elif int(ex) == 3:
        x = np.arange(-2, 2.05, 0.05)
        y = np.arange(-2, 2.05, 0.05)
        X = np.meshgrid(x, y)
        XY =np.array([x,y])# Retorna matrizes de cordenadas
        func = funcoes.func3
        break
    else: print("Escolha entre 1,2 e 3\n")
Z = func(X)  #  Avalia a função em todos os pontos - Para plotagem (meshgrid)
z = func(XY) #  Avalia a função em todos os pontos - Valores da função (Verificar máximos e mínimos)
#--------------------------------------------------------------------
modelos = AlgoritmoGenetico.gera_modelos(np.array([[x[0], x[-1]], [x[0], x[-1]]]), func)
for modelo in modelos:
    for i in range(10):
        modelo.run(stop_when_reached = float(min(z) + 1e-4) if min(z) is not None else None) #Critério de parada
#-------------------------------------------------------------
#Plotagens para relatório
plotagem.plota_3D(X[0], X[1], Z) #Plota o gráfico

