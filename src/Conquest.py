#Hay que hacer dijkstra y despues tsp sobre el subgrafo resultante
import networkx as nx
from itertools import permutations
from matplotlib import pyplot as plt;

def steiner_path(graph, terminals):
    min_cost = float('inf')
    min_path = None

    for permuted_terminals in permutations(terminals):
        path_cost = 0
        current_path = []

        for i in range(len(permuted_terminals) - 1):
            source, target = permuted_terminals[i], permuted_terminals[i + 1]
            # Find the shortest path between consecutive terminals
            shortest_path = nx.shortest_path(graph, source=source, target=target, weight='weight')
            current_path.extend(shortest_path[:-1])  # Avoid duplicating common nodes
            path_cost += nx.shortest_path_length(graph, source=source, target=target, weight='weight')

        if path_cost < min_cost:
            min_cost = path_cost
            min_path = current_path + [terminals[-1]]

    return min_path, min_cost

def plot_graph_with_path(graph, path):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, node_color='lightblue')
    
    edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    edge_labels = {(path[i], path[i+1]): graph[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)}

    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='red', node_size=700)
    nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.show()

# Example usage:
G = nx.Graph()
G.add_weighted_edges_from([(1, 2, 4), (1, 3, 2), (1, 4, 7),
                           (2, 3, 5), (2, 5, 8),
                           (3, 4, 1), (3, 5, 3),
                           (4, 6, 6),
                           (5, 6, 9),
                           (6,7,2), (6,2,6),
                           (7,1,2), (7,2,6)])

terminals = [7, 3, 5]
optimal_path, total_cost = steiner_path(G, terminals)

print("Optimal Path:", optimal_path)
print("Total Cost:", total_cost)

plot_graph_with_path(G, optimal_path)