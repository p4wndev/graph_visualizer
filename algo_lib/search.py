import streamlit as st

def bfs(graph, start_node):
    visited = set()
    queue = [start_node]
    list_nodes = []
    st.markdown("<p>Thứ tự duyệt theo chiều rộng: </p>",
                unsafe_allow_html=True)
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        list_nodes.append(node)
        neighbors = list(graph.neighbors(node))
        neighbors.sort()
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
    st.subheader(' → '.join(list_nodes))
    st.divider()
    return visited
    # drawGraph(graph)

# Duyệt đồ thị theo chiều sâu


def dfs(graph, start_node):
    visited = set()
    stack = [start_node]
    list_nodes = []
    st.markdown("<p>Thứ tự duyệt theo chiều sâu: </p>",
                unsafe_allow_html=True)
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        list_nodes.append(node)
        neighbors = list(graph.neighbors(node))
        neighbors.sort()
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(neighbor)
    st.subheader(' → '.join(list_nodes))
    st.divider()
    return visited
    # drawGraph(graph)