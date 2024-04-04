import streamlit as st


def bellman_ford(graph, start_node, edges):
    # Khởi tạo từ điển đường đi ngắn nhất
    shortest_paths = {node: float('inf') for node in graph.nodes}
    shortest_paths[start_node] = 0

    for _ in range(len(graph.nodes) - 1):
        for edge in edges:
            if len(edge) == 1:
                continue
            start, end, weight = edge[0], edge[1], edge[2]
            if shortest_paths[start] + int(weight) < shortest_paths[end]:
                shortest_paths[end] = shortest_paths[start] + int(weight)

    # Kiểm tra chu trình trọng số âm
    for edge in edges:
        if len(edge) == 1:
            continue
        start, end, weight = edge[0], edge[1], edge[2]
        if shortest_paths[start] + int(weight) < shortest_paths[end]:
            st.toast('Đồ thị chứa chu trình trọng số âm!', icon='⚠️')

    return shortest_paths

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