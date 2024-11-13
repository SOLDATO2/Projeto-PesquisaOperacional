import random
import networkx as nx
import matplotlib.pyplot as plt
import time

# Lista de todos os bairros
cidades = ["CIC", "Sítio Cercado", "Cajuru", "Boqueirão", "Uberaba", "Portão", "Alto da XV", "Santa Felicidade", "Batel", "Água Verde"]

# Dicionário de distâncias entre cada par de bairros
distancias = {
    "CIC": {"Sítio Cercado": 15, "Cajuru": 12, "Boqueirão": 10, "Uberaba": 9, "Portão": 11, "Alto da XV": 14, "Santa Felicidade": 16, "Batel": 13, "Água Verde": 17},
    "Sítio Cercado": {"CIC": 15, "Cajuru": 8, "Boqueirão": 7, "Uberaba": 6, "Portão": 13, "Alto da XV": 12, "Santa Felicidade": 14, "Batel": 9, "Água Verde": 10},
    "Cajuru": {"CIC": 12, "Sítio Cercado": 8, "Boqueirão": 5, "Uberaba": 4, "Portão": 10, "Alto da XV": 6, "Santa Felicidade": 11, "Batel": 7, "Água Verde": 9},
    "Boqueirão": {"CIC": 10, "Sítio Cercado": 7, "Cajuru": 5, "Uberaba": 3, "Portão": 9, "Alto da XV": 8, "Santa Felicidade": 12, "Batel": 7, "Água Verde": 5},
    "Uberaba": {"CIC": 9, "Sítio Cercado": 6, "Cajuru": 4, "Boqueirão": 3, "Portão": 8, "Alto da XV": 7, "Santa Felicidade": 10, "Batel": 6, "Água Verde": 5},
    "Portão": {"CIC": 11, "Sítio Cercado": 13, "Cajuru": 10, "Boqueirão": 9, "Uberaba": 8, "Alto da XV": 9, "Santa Felicidade": 8, "Batel": 4, "Água Verde": 6},
    "Alto da XV": {"CIC": 14, "Sítio Cercado": 12, "Cajuru": 6, "Boqueirão": 8, "Uberaba": 7, "Portão": 9, "Santa Felicidade": 10, "Batel": 5, "Água Verde": 7},
    "Santa Felicidade": {"CIC": 16, "Sítio Cercado": 14, "Cajuru": 11, "Boqueirão": 12, "Uberaba": 10, "Portão": 8, "Alto da XV": 10, "Batel": 6, "Água Verde": 5},
    "Batel": {"CIC": 13, "Sítio Cercado": 9, "Cajuru": 7, "Boqueirão": 7, "Uberaba": 6, "Portão": 4, "Alto da XV": 5, "Santa Felicidade": 6, "Água Verde": 3},
    "Água Verde": {"CIC": 17, "Sítio Cercado": 10, "Cajuru": 9, "Boqueirão": 5, "Uberaba": 5, "Portão": 6, "Alto da XV": 7, "Santa Felicidade": 5, "Batel": 3}
}

# GRAFO
grafo = nx.Graph()

for cidade, destinos in distancias.items():
    for destino, distancia in destinos.items():
        grafo.add_edge(cidade, destino, weight=distancia)

pos = nx.circular_layout(grafo)
nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
edge_labels = nx.get_edge_attributes(grafo, 'weight')
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)

plt.title("Grafo das Distâncias entre Cidades")
plt.show()

##################### MÉTODO DAS FORMIGAS ######################
alpha = 1.0 #importancia do feromonio
beta = 5.0 #importancia da distancia
evaporation_rate = 0.001 #taxa de evaporação 
n_ants = 10
n_iterations = 100

# Atribuindo feromônio base "1" para as cidades
feromonios = {cidade: {destino: 1.0 for destino in distancias[cidade]} for cidade in cidades}

# Função que encontra a solução para cada formiga
def construir_rota(cidade_inicial):
    rota = [cidade_inicial]
    cidades_restantes = cidades.copy()
    cidades_restantes.remove(cidade_inicial) #remove a cidade de inicio pois ja passamos por ela

    while cidades_restantes:
        cidade_atual = rota[-1] #pega a cidade atual
        probabilidade = []
        # Fórmula 1
        for cidade in cidades_restantes:
            tau = feromonios[cidade_atual][cidade] ** alpha
            #tau representa o nivel de feromonio entre a cidade atual e a cidade destino
            eta = (1.0 / distancias[cidade_atual][cidade]) ** beta
            #eta representa a atratividade do caminho
            probabilidade.append(tau * eta)
        
        total_probabilidade = sum(probabilidade)
        probabilidade = [p / total_probabilidade for p in probabilidade]
        
        proxima_cidade = random.choices(cidades_restantes, probabilidade)[0]
        rota.append(proxima_cidade)
        cidades_restantes.remove(proxima_cidade)

    rota.append(cidade_inicial)
    return rota

# Calcula o custo da rota
def calcular_custo(rota):
    return sum(distancias[rota[i]][rota[i + 1]] for i in range(len(rota) - 1))

# Função principal do ACO
def aco():
    melhor_rota, melhor_custo = None, float('inf')
    for _ in range(n_iterations):
        todas_rotas = [ #forma uma lista que contem uma lista de strings que formam uma rota em sequencia
                        #e no fim o custo da rota
            #(['Água Verde', 'Batel', 'Portão', 'Alto da XV', 'Uberaba', 'Boqueirão', 'Cajuru', 'Sítio Cercado', 'Santa Felicidade', 'CIC', 'Água Verde'], 82)
            #...
            #isso se repete 10 vezes para as 10 formigas
            (construir_rota(random.choice(cidades)), calcular_custo(construir_rota(random.choice(cidades)))) for _ in range(n_ants)
            
            ]
        #armazena a rota com o menor custo
        for rota, custo in todas_rotas:
            if custo < melhor_custo:
                melhor_rota, melhor_custo = rota, custo
        
        # Atualizar feromônios
        # Fórmula 2
        for rota, custo in todas_rotas:
            for i in range(len(rota) - 1):
                feromonios[rota[i]][rota[i + 1]] += 1.0 / custo
        
        # Evaporação
        # Fórmula 3
        for cidade in feromonios:
            for destino in feromonios[cidade]:
                feromonios[cidade][destino] *= (1 - evaporation_rate)

    return melhor_rota, melhor_custo

###### MÉTODO VIZINHO MAIS PRÓXIMO ######
def vizinho_mais_proximo(cidade_inicial):
    rota, cidades_restantes = [cidade_inicial], cidades.copy()
    cidades_restantes.remove(cidade_inicial)

    while cidades_restantes:
        cidade_atual = rota[-1]
        cidade_mais_proxima = min(cidades_restantes, key=lambda cidade: distancias[cidade_atual][cidade])
        rota.append(cidade_mais_proxima)
        cidades_restantes.remove(cidade_mais_proxima)

    rota.append(cidade_inicial)
    return rota, calcular_custo(rota)

# Execução dos algoritmos
inicio_aco = time.time()
melhor_rota_aco, melhor_custo_aco = aco()
fim_aco = time.time()

inicio_vmp = time.perf_counter()
melhor_rota_vmp, melhor_custo_vmp = vizinho_mais_proximo(random.choice(cidades))
fim_vmp = time.perf_counter()








# Resultado ACO
print(f"Rota ótima (ACO): {melhor_rota_aco}")
print(f"Custo da rota (ACO): {melhor_custo_aco} km")
plt.figure(figsize=(12, 6))
nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
for i in range(len(melhor_rota_aco) - 1):
    nx.draw_networkx_edges(grafo, pos, edgelist=[(melhor_rota_aco[i], melhor_rota_aco[i + 1])], edge_color='red', width=2)
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=nx.get_edge_attributes(grafo, 'weight'))
plt.title(f"Grafo com a Melhor Rota (ACO): Custo = {melhor_custo_aco} km")
plt.show()

print(f"Tempo de execução do ACO: {fim_aco - inicio_aco} segundos")







# Resultado Vizinho Mais Próximo
print(f"Rota ótima (Vizinho Mais Próximo): {melhor_rota_vmp}")
print(f"Custo da rota (Vizinho Mais Próximo): {melhor_custo_vmp} km")
plt.figure(figsize=(12, 6))
nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
for i in range(len(melhor_rota_vmp) - 1):
    nx.draw_networkx_edges(grafo, pos, edgelist=[(melhor_rota_vmp[i], melhor_rota_vmp[i + 1])], edge_color='blue', width=2)
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=nx.get_edge_attributes(grafo, 'weight'))
plt.title(f"Grafo com a Melhor Rota (Vizinho Mais Próximo): Custo = {melhor_custo_vmp} km")
plt.show()

tempo_execucao_vmp = fim_vmp - inicio_vmp
print(f"Tempo de execução do Vizinho Mais Próximo: {tempo_execucao_vmp:.10f} segundos")
