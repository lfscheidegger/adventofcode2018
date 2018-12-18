from collections import defaultdict

import numpy as np

def adjacency(position):
    return ((x[0] + position[0], x[1] + position[1]) for x in [(0, -1), (-1, 0), (1, 0), (0, 1)])

def find_paths_to_in_range(initial, board, actors):
    for idx in range(len(board)):
        board[idx] = board[idx].replace("G", ".").replace("E", ".")
    for actor in actors:
        actor_line = board[actor.position[1]]
        board[actor.position[1]] = actor_line[:actor.position[0]] + actor.type + actor_line[actor.position[0] + 1:]

    width = len(board[0])
    height = len(board)

    # First, find all actual 'vertices' in the graph
    nodes = []
    for y in range(height):
        for x in range(width):
            tile = board[y][x]
            if tile == '.' or (x, y) == initial:
                nodes.append((x, y))

    # Then, build all 'edges'
    edges = defaultdict(list)
    for node_idx in range(len(nodes)):
        node = nodes[node_idx]
        for adj in adjacency(node):
            if adj not in nodes:
                continue
            neighbor_idx = nodes.index(adj)
            neighbor = nodes[neighbor_idx]
            edges[node].append(neighbor)

    visited = {initial: 0}
    path = {}

    nodes = set(nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
                    
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        
        for edge in edges[min_node]:
            weight = current_weight + 1
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = [min_node]
            elif edge in visited and weight == visited[edge]:
                path[edge].append(min_node)

    return visited, path
