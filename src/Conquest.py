#Hay que hacer dijkstra y despues tsp sobre el subgrafo resultante
import networkx as nx
from matplotlib import pyplot as plt;

def subgrafo(grafo: nx.Graph, sistplan: set[int]):
    
    aristas = []
    dictarista_recorrido = dict()

    for i in sistplan:
        distancias, caminos  = nx.single_source_dijkstra(grafo, source=i)
        listarecorridos = []
        for r in caminos:
            origen = caminos[r][0] 
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
        dictarista_recorrido[origen] = [tuple(k for k in r[2]) for r in listarecorridos]

    grafores = nx.Graph()
    grafores.add_weighted_edges_from(aristas)

    return grafores, dictarista_recorrido

def recorrido_minimo(grafo: nx.Graph, dicc: dict[list[str, tuple[str, str, list[str]]]]):
    grafoaux = grafo.to_directed()
    a = nx.tournament.hamiltonian_path(grafoaux)
    print(a)

def arbol_minimo(grafo: nx.Graph, dicc: dict[list[str, tuple[str, str, list[str]]]]):
    grafoaux = grafo.to_directed()
    a = nx.tournament.hamiltonian_path(grafoaux)
    print(a)

def asocia(lista: list,dicc: dict[list[str, tuple[str, str, list[str]]]]):
    asocia

def main():
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

    # Definir el conjunto de destinos
    destinos = {"C", "D", "E", "H", "G"}

    G2, diccrecorr = subgrafo(G, destinos)

    recorrido_minimo(G2, diccrecorr)

    pos = nx.spring_layout(G)  # Layout para posicionar los nodos
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold")
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

    # Visualizar G, coloreando los nodos que también aparecen en G2 de manera diferente
    node_colors_G = ["yellow" if nodo in G2.nodes else "skyblue" for nodo in G.nodes]
    nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors_G, font_size=10, font_color="black", font_weight="bold")
    labels_G = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_G)
    plt.show()

if __name__ == "__main__":
    main()

