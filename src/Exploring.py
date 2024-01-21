#Establecemos un criterio de evaluacion(Distancia al punto de corte, así como la cantidad de sectores que aisla el punto)
from matplotlib import pyplot as plt
import networkx as nx
import Reader
import Loader
import math

def puntos_de_corte_y_aislamiento(grafo: nx.Graph):
    dicc = dict()
    for i in list(nx.articulation_points(grafo)):
        grafoaux = grafo.copy()
        grafoaux.remove_node(i)
        dicc[i] = sorted(nx.connected_components(grafoaux), key=len, reverse=True)[1:]
    for i in dicc:
        dicc[i] = [elemento for sublista in dicc[i] for elemento in sublista]
    return dicc

def elimina_redundancias(dicc: dict):
    diccaux = dicc.copy()
    conjunto_aislante={r[0] for r in diccaux.items()}
    conjunto_aislado={j for i in diccaux.items() for j in i[1]}
    for r in dicc:
        if r not in conjunto_aislante.difference(conjunto_aislado):
            diccaux.pop(r)
    return diccaux

def topedist(grafo: nx.Graph, numParticipantes: int):
    lis = [w[2]["weight"] for w in grafo.edges(data=True)]
    avglongitud = sum(lis)/len(lis)
    pesototal = 1.2 *sum([w[2]["weight"] for w in grafo.edges(data=True)])
    #print("peso medio por arista: " + str(pesomedio))
    pesoporpart = pesototal/numParticipantes
    #print("peso correspondiente por participante (mas 20%): " + str(pesoporpart))
    #print("grado medio: " + str((g.number_of_edges()*2)/g.number_of_nodes()))
    saltos = math.log(pesoporpart, ((grafo.number_of_edges()*2)/grafo.number_of_nodes()-1))
    #print("podemos apostar con cierto margen de seguridad aristas a este numero de saltos " + str(saltos))
    #Colorear el mapa por distancia a nodos origen (si estan a max) distancia*pesomedio 
    #print("podemos apostar con cierto margen de seguridad aristas a esta distancia " + str(saltos*pesomedio))
    return saltos*avglongitud

def rankea(grafo: nx.Graph, dicc_corte: dict, numpart: int):
    ranking = dict()
    toped = topedist(grafo, numpart)
    for i in grafo.nodes():
        punt=0
        for j in dicc_corte:
            dist = nx.shortest_path_length(grafo, i, j)
            if dist<toped:
                punt+=len(dicc_corte[j])*dist/toped
        ranking[i] = punt
    return ranking

def main():
    dicc_completo = Reader.lectura("./output/output0.json")
    grafo = Loader.genera_grafo(dicc_completo)
    grafosimpleponderado = Loader.adjudica_pesos(grafo, dicc_completo)
    grafosimpleponderadoposicionado = Loader.adjudica_posiciones(grafosimpleponderado, dicc_completo)
    g = Loader.adjudica_etiquetas(grafosimpleponderadoposicionado, dicc_completo)
    
    print("")
    print("test 1")
    print("")
    a = puntos_de_corte_y_aislamiento(g)

    for r in a:
        print(str(r) +  ":" + ((3-len(str(r)))*" ") +str(a[r]))

    b = elimina_redundancias(a)
    print("")
    print("test 2")
    print("")
    for r in b:
        print(str(r) + ": " + ((3-len(str(r)))*" ") + str(b[r]))

    print("test 3")
    c = topedist(g, 10)
    print(c)

    print("test 4")
    d = rankea(g, a, 10)
    print(d)
    
    posiciones = {nodo: (g.nodes[nodo]['x'], g.nodes[nodo]['y']) for nodo in g.nodes}
    nx.draw(g, pos=posiciones, labels=nx.get_node_attributes(g, "Label"), font_size=8, )
    plt.show()


if __name__ == "__main__":
    main()

#Aplicamos heuristicas
