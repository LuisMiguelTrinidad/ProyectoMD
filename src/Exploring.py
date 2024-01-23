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
    pesoporpart = pesototal/numParticipantes
    saltos = math.log(pesoporpart, ((grafo.number_of_edges()*2)/grafo.number_of_nodes()-1))
    return saltos*avglongitud

def rankea(grafo: nx.Graph, dicc_corte: dict, numpart: int):
    ranking = dict()
    toped = topedist(grafo, numpart)
    for i in grafo.nodes():
        punt=0
        for j in dicc_corte:
            dist = nx.shortest_path_length(grafo, i, j, weight="weight")
            if dist<toped:
                punt+=(len(dicc_corte[j])*(toped-dist)/toped)
        ranking[i] = punt
    return ranking

def destinos_posibles(grafo: nx.Graph, puntoinicio: int,participantes: int):
    grafoaux = grafo.copy()
    distancias, caminos = nx.single_source_dijkstra(grafoaux, puntoinicio)
    limite = topedist(grafo, participantes)
    destinos = puntos_de_corte_y_aislamiento(grafo)
    for r in distancias:
        if(distancias[r]>limite):
            grafoaux.remove_node(r)
        if (r not in destinos or distancias[r]>limite):
            caminos.pop(r)
    
    return grafoaux, caminos

#Primer destino
def explora(grafo: nx.Graph, dicc_corte: dict, numpart: int, origen:int):
    toped = topedist(grafo, numpart)
    pesos, caminos = nx.single_source_dijkstra(grafo,origen)
    pesos = {r: pesos[r] for r in pesos if r in dicc_corte and r != origen}
    caminos = {r: caminos[r] for r in caminos if r in dicc_corte and r != origen}
    puntuacion_lista = dict()
    for i in pesos:
        if pesos[i]<toped:
            puntuacion_lista[i] = (len(dicc_corte[i])*(toped-pesos[i])/toped)
    for i in caminos:
        for j in caminos[i]:
            if i in puntuacion_lista and j in puntuacion_lista and puntuacion_lista[i]<puntuacion_lista[j] and i in dicc_corte[j]:
                puntuacion_lista.pop(i)
    return puntuacion_lista



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
    #for r in a:
    #    print(str(r) +  ":" + ((3-len(str(r)))*" ") +str(a[r]))

    b = elimina_redundancias(a)
    print("")
    print("test 2")
    print("")
    for r in b:
        print(str(r) + ": " + ((3-len(str(r)))*" ") + str(b[r]))

    print("")
    print("test 3")
    print("")
    c = topedist(g, 10)
    print(c)

    print("test 4")
    d = rankea(g, b, 10)
    #for r in d:
    #    print(str(r) + ": " + ((3-len(str(r)))*" ") + str(d[r]))
    
    maximo = max([d[an] for an in d])
    
    nodo_posiciones = {nodo: (g.nodes[nodo]['x'], g.nodes[nodo]['y']) for nodo in g.nodes}
    nodo_colores = [(2 * (1 - (d[r] / maximo)), 1, 0.15) if d[r]/maximo > 0.5 else (1, 2 * (d[r] / maximo), 0.15) for r in d]
    nodo_tamano = [18*(8+r[1]) for r in d.items()]
    nx.draw(g,with_labels=True, pos=nodo_posiciones, font_size=8, node_color=nodo_colores, node_size=nodo_tamano)
    plt.show()

    listaordenada = [(r[0], 10*r[1]/maximo) for r in sorted(d.items(),key=lambda a:a[1], reverse=True)]
    print("Imprimiento los diez mejores sistemas")
    for r in range(10):
        print(listaordenada[r])

    print("Imprimiento los diez peores sistemas")
    for r in range(10):
        print(listaordenada[-(r+1)])

    subg, caminos = destinos_posibles(g, 130, 10)

    destinos = puntos_de_corte_y_aislamiento(g).keys()

    print("Hola")
    ef = sorted(explora(g, a, 10, 130).items(), key=lambda a:a[1], reverse=True)
    [print(r) for r in ef]

    conjunto = set()
    for r in caminos:
        if caminos[r][-1] in destinos:
            conjunto.update([(caminos[r][k], caminos[r][k+1]) for k in range(len(caminos[r])-1)])
    nodo_colores = [
        "#DF954B" if (r in a.keys() and r in subg.nodes())
        else "red" if r == 130 
        else "#9AB5C6" if r in subg.nodes() 
        else "#F0F0F0" for r in g.nodes()]
    arista_colores = [
        "#DF954B" if ((r[0],r[1]) in conjunto or (r[1],r[0]) in conjunto) 
        else "#9AB5C6" if r in subg.edges() 
        else  "#F0F0F0" for r in g.edges()]
    arista_tamano = [
        6 if ((r[0],r[1]) in conjunto or (r[1],r[0]) in conjunto) 
        else 3 if r in subg.edges() 
        else 1 for r in g.edges()]
    nodo_etiquetas={r: r if r in subg.nodes() else "" for r in g.nodes()}
    nodo_tamano = [
        300 if r in subg.nodes() and r in a.keys() 
        else 250 if r in subg.nodes()
        else 70 for r in g.nodes()]
    nx.draw(g, node_size=nodo_tamano, labels=nodo_etiquetas, pos=nodo_posiciones, node_color=nodo_colores, edge_color=arista_colores, width=arista_tamano)
    plt.xlim(-360,360)
    plt.ylim(-360,360)
    plt.show()

    print("Hola")
    ef = explora(g, a, 10, 130)
    [print(r) for r in ef]

    conjunto = set()
    for r in ef:
        if caminos[r][-1] in ef:
            conjunto.update([(caminos[r][k], caminos[r][k+1]) for k in range(len(caminos[r])-1)])
    nodo_colores = [
        "#DF954B" if (r in ef.keys() and r in subg.nodes())
        else "red" if r == 130 
        else "#9AB5C6" if r in subg.nodes() 
        else "#F0F0F0" for r in g.nodes()]
    arista_colores = [
        "#DF954B" if ((r[0],r[1]) in conjunto or (r[1],r[0]) in conjunto) 
        else "#9AB5C6" if r in subg.edges() 
        else  "#F0F0F0" for r in g.edges()]
    arista_tamano = [
        6 if ((r[0],r[1]) in conjunto or (r[1],r[0]) in conjunto) 
        else 3 if r in subg.edges() 
        else 1 for r in g.edges()]
    nodo_etiquetas={r: r if r in subg.nodes() else "" for r in g.nodes()}
    nodo_tamano = [
        300 if r in subg.nodes() and r in ef.keys() 
        else 250 if r in subg.nodes()
        else 70 for r in g.nodes()]
    nx.draw(g, node_size=nodo_tamano, labels=nodo_etiquetas, pos=nodo_posiciones, node_color=nodo_colores, edge_color=arista_colores, width=arista_tamano)
    plt.xlim(-360,360)
    plt.ylim(-360,360)
    plt.show()

    

if __name__ == "__main__":
    main()

#Aplicamos heuristicas
