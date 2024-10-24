import random
import networkx as nx
import matplotlib.pyplot as plt
import time

cidades = ["CIC", "Sítio Cercado", "Cajuru", "Boqueirão", "Uberaba"]

distancias = {
    "CIC": {"Sítio Cercado": 15, "Cajuru": 12, "Boqueirão": 10, "Uberaba": 9},
    "Sítio Cercado": {"CIC": 15, "Cajuru": 8, "Boqueirão": 7, "Uberaba": 6},
    "Cajuru": {"CIC": 12, "Sítio Cercado": 8, "Boqueirão": 5, "Uberaba": 4},
    "Boqueirão": {"CIC": 10, "Sítio Cercado": 7, "Cajuru": 5, "Uberaba": 3},
    "Uberaba": {"CIC": 9, "Sítio Cercado": 6, "Cajuru": 4, "Boqueirão": 3}
}

#GRAFO
grafo = nx.Graph()

for cidade, destinos in distancias.items():
    for destino, distancia in destinos.items():
        grafo.add_edge(cidade, destino, weight=distancia)


pos = nx.spring_layout(grafo)
nx.draw(grafo, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold', edge_color='gray')
edge_labels = nx.get_edge_attributes(grafo, 'weight')
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)

# Mostrar o grafo
plt.title("Grafo das Distâncias entre Cidades")
plt.show()



alpha = 1.0
beta = 5.0
evaporation_rate = 0.001
n_ants = 5
n_iterations = 10000

# Inicialização de feromônios
feromonios = {}
for cidade in cidades:
    feromonios[cidade] = {}
    for destino in distancias[cidade]:
        feromonios[cidade][destino] = 1.0
        
    #feromonios = {CIC: {Sítio Cercado: 1.0, Cajuru: 1.0, Boqueirão: 1.0, Uberaba: 1.0}
    # .
    # .

# Função para construir uma solução para cada formiga
def construir_rota(cidade_inicial):
    rota = [cidade_inicial]
    cidades_restantes = cidades.copy()
    cidades_restantes.remove(cidade_inicial)

    while len(cidades_restantes) > 0:
        cidade_atual = rota[-1]
        probabilidade = []
        
        for cidade in cidades_restantes:
            tau = feromonios[cidade_atual][cidade] ** alpha
            eta = (1.0 / distancias[cidade_atual][cidade]) ** beta
            probabilidade.append(tau * eta)
        
        total_probabilidade = sum(probabilidade)
        
        for i in range(len(probabilidade)):
            probabilidade[i] /= total_probabilidade
        
        proxima_cidade = random.choices(cidades_restantes, probabilidade)[0]
        rota.append(proxima_cidade)
        cidades_restantes.remove(proxima_cidade)

    rota.append(cidade_inicial)  # Fechar o circuito
    return rota

# Função para calcular o custo de uma rota
def calcular_custo(rota):
    custo = 0
    for i in range(len(rota) - 1):
        custo += distancias[rota[i]][rota[i + 1]]
    return custo

# Função principal do ACO
def aco():
    melhor_rota = None
    melhor_custo = float('inf')
    
    inicio = time.time()
    for _ in range(n_iterations): #epocas
        todas_rotas = []
        
        for _ in range(n_ants): #para cada formiga que existe, no caso 5.
            cidade_inicial = random.choice(cidades)
            rota = construir_rota(cidade_inicial)
            custo = calcular_custo(rota)
            todas_rotas.append((rota, custo))
            
            if custo < melhor_custo:
                melhor_rota, melhor_custo = rota, custo
        
        # Atualizar feromônios
        for rota, custo in todas_rotas:
            for i in range(len(rota) - 1):
                feromonios[rota[i]][rota[i + 1]] += 1.0 / custo
        
        # Evaporação
        for cidade in feromonios:
            for destino in feromonios[cidade]:
                feromonios[cidade][destino] *= (1 - evaporation_rate)
    fim = time.time()
    
    print(f"Tempo de execucao: {fim - inicio} s")

    return melhor_rota, melhor_custo

melhor_rota, melhor_custo = aco()
print(f"Melhor rota encontrada: {melhor_rota} com custo de {melhor_custo} km")
