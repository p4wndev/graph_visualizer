def Kruskal(graph, edges):
    parent = {node : node for node in graph.nodes}
    # tìm đỉnh gốc
    def find_root(node):
        while node != parent.get(node):
            node = parent.get(node)
        return node
    # sắp xếp các cung theo thứ tự tăng dần
    new_edges = []
    list_w = [int(edge[2]) for edge in edges]
    for _ in range(0,len(edges)):
        min_index = list_w.index(min(list_w))
        list_w[min_index] = float('inf')
        new_edges.append(edges[min_index])
    # print(new_edges)   
    sum_w = 0
    return_edges = []
    for edge in new_edges:
        u, v, w = edge[0], edge[1], edge[2]
        root_u, root_v = find_root(u), find_root(v)
        if root_u != root_v :
            return_edges.append([min(u,v), max(u,v), w])
            parent[root_v]=root_u
            sum_w = sum_w + int(w)
    return return_edges, sum_w
