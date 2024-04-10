def Kruskal(graph):
    edges = list(graph.edges)
    parent = {node : node for node in graph.nodes}
    # hàm tìm đỉnh gốc
    def find_root(node):
        while node != parent.get(node):
            node = parent.get(node)
        return node
    # sắp xếp các cung theo thứ tự tăng dần
    sort_edges = []
    list_w = [float(graph.get_edge_data(edge[0],edge[1]).get('label')) for edge in edges]
    # print(list_w)
    for _ in range(0,len(edges)):
        min_index = list_w.index(min(list_w))
        list_w[min_index] = float('inf')
        sort_edges.append(edges[min_index])
    # print(sort_edges)
    sum_w = 0
    return_edges = []
    # duyệt qua danh sách đã sắp xếp, với mỗi cặp đỉnh (u, v) tìm đỉnh gốc của chúng
    for edge in sort_edges:
        u, v = edge[0], edge[1]
        w = graph.get_edge_data(edge[0],edge[1]).get('label')
        root_u, root_v = find_root(u), find_root(v)
        # nếu đỉnh gốc của u khác v thì thêm cung (u, v)
        if root_u != root_v :
            return_edges.append([min(u,v), max(u,v), w])
            parent[root_v]=root_u
            sum_w = sum_w + float(w)
    # trả về danh sách cung của đồ thị mới và trọng lượng của cây khung
    return return_edges, sum_w

def Prim(graph, start_node):
    # sắp xếp các đỉnh theo thứ tự tăng dần
    nodes = list(graph.nodes)
    nodes.sort(reverse=False)
    # khởi tạo
    parent = {node : '' for node in nodes}
    pi = {node : float('inf') for node in nodes}
    mark = []
    pi[start_node] = 0
    
    for _ in range(1,len(nodes)):
        # tìm đỉnh chưa duyệt có pi nhỏ nhất
        min_pi = float('inf')
        for node in nodes:
            if node not in mark and pi[node] < min_pi:
                min_pi = pi[node]
                min_node = node

        mark.append(min_node)
        # cập nhật pi và parent của các đinh láng giềng chưa duyệt
        for node in nodes:
            if node not in mark :
                if graph.has_edge(node, min_node) :
                    w = float(graph.get_edge_data(min_node,node).get('label'))
                    if w < pi[node]:
                        pi[node] = w
                        parent[node] = min_node
   
    return_edges = []
    sum_w = 0
    # với mỗi đỉnh có đỉnh cha, thêm cung đi từ đỉnh cha đến nó
    for node in nodes:
        if parent[node] != '':
            w = graph.get_edge_data(parent[node],node)['label']
            return_edges.append([node, parent[node], w])
            sum_w = sum_w + float(w)
    # trả về danh sách cung của đồ thị mới và trọng lượng của cây khung
    return return_edges, sum_w

'''
testcase

1 2 5
1 3 7.07
1 4 16.55
1 5 15.52
1 6 18
2 3 5
2 4 11.07
2 5 11.05
2 6 14.32
3 4 14
3 5 14.32
3 6 18.38
4 5 3
4 6 7.62
5 6 5

'''
