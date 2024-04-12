def topo_sort(graph):
    lst = []
     # sắp xếp các đỉnh theo thứ tự tăng dần
    nodes = [int(node) for node in graph.nodes]
    nodes.sort(reverse=False)
    nodes = [str(node) for node in nodes]
    # Khởi tạo danh sách bậc vào (in-degree) cho các node
    in_degrees = {node : 0 for node in nodes}
    # Cập nhật bậc vào dựa trên các cạnh
    for node in nodes:
        for any_node in nodes:
            if graph.has_edge(any_node, node):
                in_degrees[node] = in_degrees[node] +1
    # Tạo hàng đợi gồm các node có bậc vào bằng 0
    queue = [node for node in nodes if in_degrees[node] == 0]
    # Thực hiện thuật toán Kahn
    while queue:
        node = queue.pop(0)  # Lấy và loại bỏ node đầu tiên
        lst.append(node)    # Thêm node vào thứ tự topo
        # Xử lý các node con: giảm bậc vào và thêm vào hàng đợi nếu bậc vào về 0
        for child in nodes:
            if graph.has_edge(node, child):
                in_degrees[child] = in_degrees[child] - 1
                if in_degrees[child] == 0:
                    queue.append(child)

    return lst, len(lst) == len(nodes)

def rank(graph):
     # sắp xếp các đỉnh theo thứ tự tăng dần
    nodes = [int(node) for node in graph.nodes]
    nodes.sort(reverse=False)
    nodes = [str(node) for node in nodes]
    rank = {node : 0 for node in nodes}
    # Khởi tạo danh sách bậc vào (in-degree) cho các node
    in_degrees = {node : 0 for node in nodes}
    # Cập nhật bậc vào dựa trên các cạnh
    for node in nodes:
        for any_node in nodes:
            if graph.has_edge(any_node, node):
                in_degrees[node] = in_degrees[node] +1
    # 
    S1 = [node for node in nodes if in_degrees[node] == 0]
    k = 0
    while S1:
        S2 = []
        for u in S1:
            rank[u] = k
            for v in nodes:
                if graph.has_edge(u, v):
                    in_degrees[v] = in_degrees[v] - 1
                    if in_degrees[v] == 0:
                        S2.append(v)
        S1 = S2.copy()
        k = k + 1
    rank_value = [int(_) for _ in list(rank.values())]
    list_rank = [[] for _ in range(0,max(rank_value)+1)]
    for node in nodes:
        list_rank[rank[node]].append(node)
    return list_rank
    
'''
Test case:
1 2
1 3
2 4
2 5
2 6
3 2
3 5
3 6
4 7
5 7
6 4
6 5
'''
