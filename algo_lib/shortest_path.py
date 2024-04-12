def Moore_Dijkstra(graph, start_node, finish_node):
    def _Moore_Dijkstra_(graph, start_node, finish_node):
        # sắp xếp các đỉnh theo thứ tự tăng dần
        nodes = [int(node) for node in graph.nodes]
        nodes.sort(reverse=False)
        nodes = [str(node) for node in nodes]
        # khởi tạo
        parent = {}
        pi = {node : float('inf') for node in nodes}
        mark = []
        pi[start_node] = 0
        #
        for _ in range(1, len(nodes)):
            # tìm đỉnh chưa duyệt có pi nhỏ nhất
            min_pi = float('inf')
            min_node = str()
            for node in nodes:
                if node not in mark and pi[node] < min_pi:
                    min_pi = pi[node]
                    min_node = node
            mark.append(min_node)
            # cập nhật pi và parent của các đinh láng giềng chưa duyệt
            for node in nodes:
                if node not in mark :
                    if graph.has_edge(min_node, node) :
                        w = float(graph.get_edge_data(min_node, node)['label'])
                        if w + pi[min_node] < pi[node]:
                            pi[node] = pi[min_node] + w
                            parent[node] = min_node
        # 
        path_edge = []    
        path_node = []
        # 
        current = finish_node
        while current in parent:
            path_node.append(current)
            current = parent[current]
        path_node.append(current)
        # 
        path_node_copy = path_node.copy()
        while len(path_node_copy) > 1:
            u, v = path_node_copy.pop(), path_node_copy[-1]
            if graph.has_edge(u, v):
                path_edge.append((u, v))
            if graph.has_edge(v, u):
                path_edge.append((v, u))
        # 
        return path_edge, path_node, pi[finish_node]
    
    path = _Moore_Dijkstra_(graph, start_node, finish_node)
    path_edge, path_node = path[0], path[1]
    path_graph = graph.copy() 
    path_graph.remove_edges_from(set(graph.edges)-set(path_edge)) 
    path_graph.remove_nodes_from(set(graph.nodes)-set(path_node))
    return path_graph, path[-1]

def negative_weight_cycle(graph, start_node):
    pi = {node: float('inf') for node in graph.nodes}
    parent = {}
    pi[start_node] = 0
    parent[start_node] = ''
    for _ in range(len(graph.nodes) - 1):
        for edge in graph.edges:
            if len(edge) == 1:
                continue
            u, v = edge[0], edge[1]
            w = float(graph.get_edge_data(u, v)['label'])
            if pi[u] == float('inf'):
                continue
            if (pi[u] + w) < pi[v]:
                pi[v] = pi[u] + w
                parent[v] = u
    # Kiểm tra chu trình trọng số âm
    for edge in graph.edges:
        if len(edge) == 1:
            continue
        u, v = edge[0], edge[1]
        w = float(graph.get_edge_data(u, v)['label'])
        if pi[u] == float('inf'):
            continue
        if pi[u] + w < pi[v]:
            return True
    return False    

def Bellman_Ford(graph, start_node, finish_node):
    def _Bellman_Ford_(graph, start_node, finish_node):
        pi = {node: float('inf') for node in graph.nodes}
        parent = {}
        pi[start_node] = 0
        parent[start_node] = ''
        for _ in range(len(graph.nodes) - 1):
            for edge in graph.edges:
                if len(edge) == 1:
                    continue
                u, v = edge[0], edge[1]
                w = float(graph.get_edge_data(u, v)['label'])
                if pi[u] == float('inf'):
                    continue
                if (pi[u] + w) < pi[v]:
                    pi[v] = pi[u] + w
                    parent[v] = u
        
        path_edge = []
        path_node = []
        # 
        current = finish_node
        while current in parent:
            path_node.append(current)
            current = parent[current]
        path_node.append(current)
        # 
        path_node_copy = path_node.copy()
        while len(path_node_copy) > 1:
            u, v = path_node_copy.pop(), path_node_copy[-1]
            if graph.has_edge(u, v):
                path_edge.append((u, v))
            if graph.has_edge(v, u):
                path_edge.append((v, u))
        # 
        return path_edge, path_node, pi[finish_node]
    path = _Bellman_Ford_(graph, start_node, finish_node)
    path_edge, path_node = path[0], path[1]
    path_graph = graph.copy() 
    path_graph.remove_edges_from(set(graph.edges)-set(path_edge)) 
    path_graph.remove_nodes_from(set(graph.nodes)-set(path_node))
    return path_graph, path[-1]



'''
Test Case:
1 2 9
1 6 6
1 7 15
2 3 10
6 3 18
6 5 30
6 7 -8
7 5 20
3 5 -16
5 4 11
4 3 6
3 8 19
4 8 6
5 8 16
7 8 44
'''
