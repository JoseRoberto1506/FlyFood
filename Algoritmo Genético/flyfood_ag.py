from typing import List, Dict
from random import randint, random, shuffle
from math import sqrt


def ler_arquivo() -> List[list]:
    with open("wi29.tsp", "r") as arquivo:
        dados = []
        for linha in arquivo.readlines():
            dados.append(list(linha.split()))
        for linha in dados:
            if linha[-1] == '\n':
                linha = linha[0:-1]
    
    return dados


def pegar_pontos_e_coords(plano: List[list]) -> List[str] and Dict[str, tuple]:
    pontos = []
    pontos_e_coords = {}
    for ponto in plano:
        pontos.append(ponto[0])
        pontos_e_coords[ponto[0]] = (float(ponto[1]), float(ponto[2]))

    return pontos, pontos_e_coords


def populacao_inicial(lista_pontos: List[str], tamanho_pop: int) -> List[list]:
    # Criação de população inicial
    populacao = []
    for _ in range(tamanho_pop):
        shuffle(lista_pontos)
        individuo: List[str] = lista_pontos

        if individuo not in populacao:
            populacao.append(individuo[:])
    
    return populacao


def aptidao_individuo(ind: List[str], coords: Dict[str, tuple]) -> float:
    # Cálculo da aptidão (fitness) de um único indivíduo
    custo_caminho: float = 0

    for i in range(len(ind) - 1):
        ponto_a = coords[ind[i]]
        ponto_b = coords[ind[i + 1]]
        custo_caminho += sqrt((ponto_a[0] - ponto_b[0])**2 + (ponto_a[1] - ponto_b[1])**2)

    return custo_caminho


def aptidao(pop: List[list], coordenadas: Dict[str, tuple]) -> List[float]:
    # Aptidão (fitness) de uma população
    return [aptidao_individuo(individuo, coordenadas) for individuo in pop]


def torneio(apt: List[float]) -> int:
    # Seleção por torneio
    pai1: int = randint(0, len(apt) - 1)
    pai2: int = randint(0, len(apt) - 1)
    
    return pai1 if apt[pai1] < apt[pai2] else pai2


def selecionar_pais(populacao: List[list], aptidoes: List[float]) -> List[list]:
    # Seleção dos pais
    lista_pais: List[list] = [[None]] * len(populacao)
    for i in range(len(populacao)):
        idex_selecionado: int = torneio(aptidoes)
        lista_pais[i]: List[str] = populacao[idex_selecionado]
    
    return lista_pais


def pmx(pai_s: List[str], pai_t: List[str], tx_crossover: float) -> List[str]:
    # PMX para o crossover entre dois pais
    if random() <= tx_crossover:
        ponto_corte: int = randint(1, len(pai_s) - 2) # O ponto de corte deve estar entre o segundo e o penúltimo index
        filho: List[str] = pai_s[:]
        for i in range(ponto_corte):
            idx: int = pai_s.index(pai_t[i])
            filho[i], filho[idx] = filho[idx], filho[i]
        return filho
    
    return pai_s


def crossover(pais: List[list], tx_crossover: float) -> List[list]:
    # Crossover de todos os pais
    lista_filhos: List[list] = [[None]] * len(pais)
    n_pais: int = len(pais)
    for i in range(0, n_pais, 2):
        filho_1: List[str] = pmx(pais[i], pais[i + 1], tx_crossover)
        filho_2: List[str] = pmx(pais[i + 1], pais[i], tx_crossover)
        lista_filhos[i], lista_filhos[i + 1] = filho_1, filho_2
    
    return lista_filhos


def mutacao_individuo(ind: List[str], tx_mutacao: float) -> List[str]:
    # Mutação de um indivíduo
    if random() <= tx_mutacao:
        # Gerar dois indíces aleatórios para trocar dois pontos de posição
        index_aleatorio_1 = randint(0, len(ind) - 1)
        index_aleatorio_2 = randint(0, len(ind) - 1)
        ind[index_aleatorio_1], ind[index_aleatorio_2] = ind[index_aleatorio_2], ind[index_aleatorio_1]
    
    return ind


def mutacao(filhos: List[list], tx_mutacao: float) -> List[list]:
    # Mutação de todos os filhos
    for i, individuo in enumerate(filhos):
        filhos[i] = mutacao_individuo(individuo, tx_mutacao)
    
    return filhos


def selecao_sobreviventes(pop: List[list], apt_pop: List[float], 
                          filhos: List[list], apt_filhos: List[float], 
                          elitismo: bool) -> List[list] and List[float]:
    # Substituição geracional com elitismo
    if elitismo == True:
        index_melhor_pai = apt_pop.index(min(apt_pop))
        index_pior_filho = apt_filhos.index(max(apt_filhos))
        filhos[index_pior_filho], apt_filhos[index_pior_filho] = pop[index_melhor_pai], apt_pop[index_melhor_pai]

    # Substituição geracional sem elitismo
    return filhos, apt_filhos


def evolucao():
    """Algoritmo genético"""
    pontos_entrega, coordenadas = pegar_pontos_e_coords(ler_arquivo())
    n_pop = len(pontos_entrega) * 4 # Quantidade de permutações/caminhos
    # Taxa cruzamento = entre 0.6 e 0.9 | Taxa de mutação = aproximadamente 0.01
    n_geracoes, taxa_cruzamento, taxa_mutacao = 16000, 0.8, 0.01

    pop: List[list] = populacao_inicial(pontos_entrega, n_pop)
    apt: List[float] = aptidao(pop, coordenadas)

    for i in range(n_geracoes):
        pais: List[list] = selecionar_pais(pop, apt)
        filhos: List[list] = crossover(pais, taxa_cruzamento)
        filhos: List[list] = mutacao(filhos, taxa_mutacao)
        apt_filhos: List[float] = aptidao(pop, coordenadas)
        pop, apt = selecao_sobreviventes(pop, apt, filhos, apt_filhos, True)

    melhor_aptidao: float = min(apt)
    print(
        f"\n\n>>> Melhor solução encontrada é {pop[apt.index(melhor_aptidao)]} com função objetivo de {melhor_aptidao}\n\n")


if __name__ == "__main__":
    evolucao()
