#Hay que hacer dijkstra y despues tsp sobre el subgrafo resultante
import networkx as nx
from matplotlib import pyplot as plt;
from scipy import optimize;

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
                    print("Imprimiento listarecorridos ")
                    print(listarecorridos)      
        dictarista_recorrido[origen] = [tuple(k for k in r[2]) for r in listarecorridos]

    grafores = nx.Graph()
    grafores.add_weighted_edges_from(aristas)
    return grafores, dictarista_recorrido

def remapea(grafo: nx.Graph):
    aristas = []
    for i in grafo.nodes():
        #Distancia desde todos los puntos hasta nuestro punto i
        distancias, caminos  = nx.single_source_dijkstra(grafo, source=i)
        for r in caminos:
            origen = caminos[r][0] 
            destino = r
            distancia = distancias[r]
            if(origen!=destino):
                aristas.append((origen, destino, distancia))
    grafores = nx.Graph()
    grafores.add_weighted_edges_from(aristas)
    return grafores
    

def recorrido_minimo(grafo: nx.Graph, dicc: dict[str, list[tuple[str]]]):
    grafoaux = grafo.to_directed()
    return nx.approximation.traveling_salesman_problem(grafoaux, cycle=False)

#def arbol_minimo(grafo: nx.Graph, dicc: dict[list[str, tuple[str, str, list[str]]]]):
#    grafoaux = grafo.to_directed()
#    a = nx.tournament.hamiltonian_path(grafoaux)
#    print(a)

def asocia(lista: list,dicc: dict[str, list[tuple[str]]]):

    recorrido = []
    for i in range(len(lista)-1):
        for j in range(len(dicc.get(lista[i]))):
            if lista[i+1]==dicc.get(lista[i])[j][-1]:
                recorrido.extend(dicc.get(lista[i])[j][:-1])

    print(recorrido)
    return recorrido
        

def main():

    #Creamos grafo test
    def creagrafo():
        # Crear un grafo dirigido
        G = nx.Graph()

        # Agregar nodos al grafo
        G.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R"])

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
        G.add_edge("A", "I", weight=3)
        G.add_edge("B", "J", weight=6)
        G.add_edge("C", "K", weight=8)
        G.add_edge("D", "L", weight=4)
        G.add_edge("E", "M", weight=5)
        G.add_edge("F", "N", weight=2)
        G.add_edge("G", "O", weight=7)
        G.add_edge("H", "P", weight=1)
        G.add_edge("I", "J", weight=9)
        G.add_edge("J", "K", weight=10)
        G.add_edge("K", "L", weight=3)
        G.add_edge("L", "M", weight=7)
        G.add_edge("M", "N", weight=5)
        G.add_edge("N", "O", weight=6)
        G.add_edge("O", "P", weight=4)
        G.add_edge("P", "Q", weight=8)
        G.add_edge("Q", "R", weight=9)
        G.add_edge("R", "A", weight=2)
        G.add_edge("A", "I", weight=3)
        G.add_edge("B", "J", weight=6)
        return G

    G = creagrafo()
    # Definir el conjunto de destinos
    destinos = {"C", "D", "E", "N", "R", "P"}

    #Test 1
    G2, diccrecorr = subgrafo(G, destinos)

    #Test 2
    G3 = remapea(G2)
    print("test2")
    print(nx.to_dict_of_lists(G3))


    #Test 3
    recorrido = recorrido_minimo(G3, diccrecorr)
    print(recorrido)

    #Test 4
    #Tengo que corregir para el caso de que haya aristas raras tras remapear
    print(asocia(recorrido, diccrecorr))


    #Grafo original
    
    # Visualizar G, coloreando los nodos que también aparecen en G2 de manera diferente
    pos = nx.spring_layout(G)  # Layout para posicionar los nodos
    node_colors_G = ["yellow" if nodo in G2.nodes else "skyblue" for nodo in G.nodes]
    nx.draw(G, pos, with_labels=True, node_size=700, node_color=node_colors_G, font_size=10, font_color="black", font_weight="bold")
    labels_G = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_G)
    plt.show()


    #Grafo reducido 

    pos2 = {r: pos[r] for r in pos if r in G2.nodes()}
    nx.draw(G2, pos2, with_labels=True, node_size=700)
    labels_G2 = nx.get_edge_attributes(G2, 'weight')
    nx.draw_networkx_edge_labels(G2, pos2, edge_labels=labels_G2)
    plt.show()

    #Grafo reducido reorganizado
    nx.draw(G3, pos2, with_labels=True, node_size=700)
    labels_G3 = nx.get_edge_attributes(G3, 'weight')
    nx.draw_networkx_edge_labels(G3, pos2, edge_labels=labels_G3)
    plt.show()


if __name__ == "__main__":
    main()

