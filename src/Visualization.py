import networkx as nx
import netwulf as nw
import matplotlib.pyplot as plt
import Loader

def genera_grafo(diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> nx.Graph:
    diccionarioaux = diccionario.copy()
    diccionarioaux = {clave: diccionarioaux[clave][1] for clave in diccionarioaux}
    grafo = nx.Graph()
    for r in diccionarioaux:
        if len(diccionarioaux[r])>0:
            grafo.add_edges_from((r, k[0]) for k in diccionarioaux[r])
    return grafo

def test_genera_grafo(diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> None:
    grafoaux = genera_grafo(diccionario)
    diccionarioaux = nx.to_dict_of_lists(grafoaux)
    [print(r[0],":",r[1]) for r in sorted(diccionarioaux.items())[:3]]
    print("...")
    [print(r[0],":",r[1]) for r in sorted(diccionarioaux.items())[-3:]]

def adjudica_pesos(grafo: nx.Graph, diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> nx.Graph:
    diccionarioaux = diccionario.copy()
    diccionarioaux = {clave: diccionarioaux[clave][1] for clave in diccionarioaux}
    grafoaux = grafo.copy()
    for origen in diccionarioaux:
        for destino, peso in diccionarioaux[origen]:
            grafoaux[origen][destino]['weight'] = peso
        
    return grafoaux

def test_adjudica_pesos(grafo: nx.Graph, diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> None:
    grafoaux = adjudica_pesos(grafo, diccionario)
    diccionarioaux = {u: [(v, data['weight']) for v, data in grafoaux[u].items()] for u in grafoaux.nodes()}
    [print(r[0],":",r[1]) for r in sorted(diccionarioaux.items())[:3]]
    print("...")
    [print(r[0],":",r[1]) for r in sorted(diccionarioaux.items())[-3:]]

def adjudica_posiciones(grafo: nx.Graph, diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> nx.Graph:
    diccionarioaux = diccionario.copy()
    diccionarioaux = {clave: diccionarioaux[clave][2] for clave in diccionarioaux}
    grafoaux = grafo.copy()
    nx.set_node_attributes(grafoaux, diccionarioaux, 'Position')
    return grafoaux

def test_adjudica_posiciones(grafo: nx.Graph, diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> None:
    grafoaux = adjudica_posiciones(grafo, diccionario)
    diccionarioaux = {u: grafoaux.nodes[u]['Position'] for u in grafoaux.nodes()}
    [print(u, ":", pos) for u, pos in sorted(diccionarioaux.items())[:3]]
    print("...")
    [print(u, ":", pos) for u, pos in sorted(diccionarioaux.items())[-3:]]

def adjudica_etiquetas(grafo: nx.Graph, diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> nx.Graph:
    diccionarioaux = diccionario.copy()
    diccionarioaux = {clave: diccionarioaux[clave][0] for clave in diccionarioaux}
    grafoaux = grafo.copy()
    nx.set_node_attributes(grafoaux, diccionarioaux, 'Label')
    return grafoaux

def test_adjudica_etiquetas(grafo: nx.Graph, diccionario: dict[int, list[tuple[int,float]],tuple[float,float]]) -> None:
    grafoaux = adjudica_etiquetas(grafo, diccionario)
    diccionarioaux = {u: grafoaux.nodes[u]['Label'] for u in grafoaux.nodes()}
    [print(u, ":", label) for u, label in sorted(diccionarioaux.items())[:3]]
    print("...")
    [print(u, ":", label) for u, label in sorted(diccionarioaux.items())[-3:]]


def main():
    print("\nRealizando lectura")
    dicc_completo = Loader.lectura("./output/output0.json")
    Loader.test_lectura(dicc_completo)
    
    print("\nRealizando carga del grafo")
    grafo = genera_grafo(dicc_completo)
    test_genera_grafo(dicc_completo)

    print("\nRealizando ponderacion del grafo")
    grafosimpleponderado = adjudica_pesos(grafo, dicc_completo)
    test_adjudica_pesos(grafo, dicc_completo)

    print("\nRealizando coordinación del grafo")
    grafosimpleponderadoposicionado = adjudica_posiciones(grafosimpleponderado, dicc_completo)
    test_adjudica_posiciones(grafosimpleponderado, dicc_completo)

    print("\nRealizando etiquetación del grafo")
    grafosimpleponderadoposicionadoetiquetado = adjudica_etiquetas(grafosimpleponderadoposicionado, dicc_completo)
    test_adjudica_etiquetas(grafosimpleponderadoposicionado, dicc_completo)
    
    



if __name__ == "__main__":
    main()
