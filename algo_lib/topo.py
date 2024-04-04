def topo_sort(graph, list, edges):

    # Khởi tạo danh sách bậc vào (in-degree) cho các node
    in_degrees = {}
    for node in graph.nodes:
        in_degrees[node] = 0

    # Cập nhật bậc vào dựa trên các cạnh
    for start, end in edges:
        in_degrees[end] += 1

    # Tạo hàng đợi các node có bậc vào bằng 0
    queue = [node for node, degree in in_degrees.items() if degree == 0]

    # Thực hiện thuật toán Kahn
    while queue:
        node = queue.pop(0)  # Lấy và loại bỏ node đầu tiên
        list.append(node)                  # Thêm node vào thứ tự topo

        # Xử lý các node con: giảm bậc vào và thêm vào hàng đợi nếu bậc vào về 0
        for child in graph[node]:
            in_degrees[child] -= 1
            if in_degrees[child] == 0:
                queue.append(child)

    # Kiểm tra chu trình
    if len(list) != len(graph.nodes):
        return []

    return list


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
