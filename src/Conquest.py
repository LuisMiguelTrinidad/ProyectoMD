#Hay que hacer dijkstra y despues tsp sobre el subgrafo resultante
import networkx as nx
from matplotlib import pyplot as plt;

def subgrafo(grafo: nx.Graph, sistplan: set[int]):
    listarecorridos = []
    aristas = []

    for i in sistplan:
        distancias, caminos  = nx.single_source_dijkstra(G, source=i)

        for r in caminos:
            origen = caminos[r][0] #El elemento 0 de la lista de vertices recorridos
            destino = r
            distancia = distancias[r]
            if(origen!=destino and destino in sistplan):
                a = True
                for destinatario in sistplan:
                    if destinatario!=origen and destinatario!=destino and destinatario in caminos[r]:
                        a = False
                if(a):        
                    aristas.append((origen, destino, distancia))
                    listarecorridos.append((origen, destino, caminos[r]))
    grafores = nx.Graph()
    grafores.add_weighted_edges_from(aristas)

    print(aristas)
    print(listarecorridos)

    pos = nx.circular_layout(grafores)  # Layout para posicionar los nodos
    nx.draw(grafores, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold")
    labels = nx.get_edge_attributes(grafores, 'weight')
    nx.draw_networkx_edge_labels(grafores, pos, edge_labels=labels)
    plt.show()


















# Crear un grafo dirigido
G = nx.Graph()

# Agregar nodos al grafo
G.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])

# Agregar aristas con pesos al grafo
G.add_edge("A", "B", weight=4)
G.add_edge("A", "C", weight=2)
G.add_edge("B", "C", weight=5)
G.add_edge("B", "D", weight=10)
G.add_edge("C", "D", weight=3)
G.add_edge("D", "E", weight=7)
G.add_edge("E", "F", weight=6)
G.add_edge("F", "G", weight=8)
G.add_edge("G", "H", weight=9)
G.add_edge("H", "A", weight=1)

# Puedes agregar más nodos y aristas según tus necesidades

# Definir el conjunto de destinos
destinos = {"C", "D", "E", "H", "G"}

pos = nx.spring_layout(G)  # Layout para posicionar los nodos
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold")
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()

subgrafo(G, destinos)
