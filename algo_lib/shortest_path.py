import streamlit as st


def bellman_ford(graph, start_node, edges):
    # Khởi tạo từ điển đường đi ngắn nhất
    shortest_paths = {node: float('inf') for node in graph.nodes}
    shortest_paths[start_node] = 0

    # Thư giãn các cạnh |V| - 1 lần
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
