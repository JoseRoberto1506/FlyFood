from time import process_time


def main():
    linhas, colunas, matriz = ler_matriz()

    pontos_de_entrega, coordenadas = pegar_pontos_de_entrega(linhas, colunas, matriz)

    inicio = process_time()

    rotas = permutar(pontos_de_entrega)

    calcular_custo_das_rotas(rotas, coordenadas)

    fim = process_time()
    print(f"Tempo total: {fim - inicio} segundos")


def ler_matriz():
    with open("matriz.txt", "r") as arquivo:
        # Pegar a quantidade de linhas e colunas da matriz
        quantidade_linhas, quantidade_colunas = arquivo.readline().split()
        
        # Ler cada linha da matriz
        matriz_lida = []
        for linha in arquivo.readlines():
            matriz_lida.append(list(linha.split()))
        
        # Remover as quebras de linha ('\n') de cada linha 
        for linha in matriz_lida:
            if linha[-1] == '\n':
                linha = linha[0:-1]
        
    return int(quantidade_linhas), int(quantidade_colunas), matriz_lida


def pegar_pontos_de_entrega(linha, coluna, Matriz):
    pontos = []
    pontos_e_coordenadas = {}

    for i in range(linha):
        for j in range(coluna):
            if Matriz[i][j].isalpha():
                pontos.append(Matriz[i][j])
                pontos_e_coordenadas[Matriz[i][j]] = (i, j)
    
    pontos.remove('R')

    return pontos, pontos_e_coordenadas


'''
def xyz(lista):
    for cada ponto não visitado
        for combinação em (xyz() - lista[0])
'''


def permutar(pontos):
    if len(pontos) == 1:
        return [pontos]
    
    # Lista para armazenar as combinações de rotas
    combinações = []

    # Travando um ponto pelo seu index na lista de pontos
    for ponto_travado in range(len(pontos)):
        pontos_restantes = pontos[0:ponto_travado] + pontos[ponto_travado + 1:]
        # Concatenando cada combinação de rota dos pontos restantes com o ponto travado
        for ponto in permutar(pontos_restantes):
            combinações.append([pontos[ponto_travado]] + ponto)

    return combinações


def calcular_distancia_entre_pontos(ponto_1, ponto_2):
    distancia = abs(ponto_1[0] - ponto_2[0]) + abs(ponto_1[1] - ponto_2[1])
    
    return distancia


def calcular_custo_das_rotas(caminhos, coords):
    custo_menor_caminho = 9999
    menor_caminho = []

    for caminho in caminhos:
        custo_caminho_atual = 0

        # Colocando o ponto de origem e retorno no caminho
        caminho.insert(0, 'R')
        caminho.append('R')

        # Calculando a distância entre os pontos adjacentes de cada caminho
        for i in range(len(caminho) - 1):
            coord_ponto_1 = coords[caminho[i]]
            coord_ponto_2 = coords[caminho[i + 1]]
            custo_caminho_atual += calcular_distancia_entre_pontos(coord_ponto_1, coord_ponto_2)

        if custo_caminho_atual < custo_menor_caminho:
            custo_menor_caminho = custo_caminho_atual
            menor_caminho = caminho

    print(f"Rota de menor distância: '{' '.join(menor_caminho)}'")
    print(f"Distância da menor rota: {custo_menor_caminho} dronômetros")


main()
