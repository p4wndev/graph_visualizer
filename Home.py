import streamlit as st
import networkx as nx
import pyvis as pv
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(layout="centered",
                   page_title="Mô phỏng đồ thị",
                   page_icon="🧠",
                   initial_sidebar_state="expanded")


# Tạo đồ thị

# Vô hướng
def createGraph(edges):
    G = nx.Graph()
    for edge in edges:
        if len(edge) == 1:
            G.add_node(edge[0])
        elif len(edge) == 2:
            G.add_edge(edge[0], edge[1], weight=1)
        elif len(edge) == 3:
            # weight = int(edge[2])
            G.edges(data=True)
            G.add_edge(edge[0], edge[1], title=edge[2], label=edge[2])
        else:
            st.toast("Cung có nhiều hơn 4 tham số sẽ không hiển thị!", icon='⚠️')
    return G

# Có hướng


def createDiGraph(edges):
    G = nx.DiGraph()
    for edge in edges:
        if len(edge) == 1:
            G.add_node(edge[0])
        elif len(edge) == 2:
            G.add_edge(edge[0], edge[1])
        elif len(edge) == 3:
            # weight = int(edge[2])
            G.add_edge(edge[0], edge[1], title=edge[2], label=edge[2])
    return G


# Duyệt đồ thị theo chiều rộng


def bfs(graph, start_node):
    visited = set()
    queue = [start_node]
    list = []

    st.markdown("<p>Thứ tự duyệt theo chiều rộng: </p>",
                unsafe_allow_html=True)
    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        list.append(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                queue.append(neighbor)
    st.subheader(' → '.join(list))
    st.divider()
    return visited
    # drawGraph(graph)


# Duyệt đồ thị theo chiều sâu
def dfs(graph, start_node):
    visited = set()
    stack = [start_node]
    list = []

    st.markdown("<p>Thứ tự duyệt theo chiều sâu: </p>",
                unsafe_allow_html=True)
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        list.append(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                stack.append(neighbor)
    st.subheader(' → '.join(list))
    st.divider()
    return visited
    # drawGraph(graph)


def tarjan(graph):
    index = {}  # Chứa chỉ số đánh số của các đỉnh
    lowlink = {}  # Chứa giá trị lowlink của các đỉnh
    stack = []  # Stack để lưu trữ các đỉnh đã duyệt
    result = []  # Danh sách các thành phần liên thông mạnh

    def dfs(v):
        index[v] = len(index)
        lowlink[v] = len(lowlink)
        stack.append(v)

        for w in graph.neighbors(v):
            if w not in index:
                dfs(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            component = []
            while True:
                w = stack.pop()
                component.append(w)
                if w == v:
                    break
            result.append(component)

    for v in graph.nodes:
        if v not in index:
            dfs(v)
        return result

def get_component_edges(edges, component):
    component_edges = []
    for edge in edges:
        if len(component) == 1:
            component_edges.append((component.pop()))
        elif (all(node in component for node in edge)):
            component_edges.append(edge)
    return component_edges


# Vẽ đồ thị


def drawGraph(graph, directed):
    vis = Network(height="350px", width="100%", directed=directed)
    vis.from_nx(graph)
    vis.write_html("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=360)


def draw_component(component):
    vis = Network(height="350px", width="100%", directed=False)
    vis.from_nx(component)
    vis.write_html("component.html")
    HtmlFile = open("component.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=425)


def main():
    # Giao diện người dùng
    st.title("✨Mô Phỏng :red[Đồ Thị]")
    # with st.sidebar.popover("Huong dan su dung"):
    #     st.write("hello")

    # Nhập danh sách cung
    st.sidebar.subheader("📝Nhập đồ thị:")
    directed = st.sidebar.toggle("Có hướng")
    edges = st.sidebar.text_area(
        "Danh sách cung (cạnh):", value="1 2 4\n2 3 5\n3 1 10")
    has_weights = False
    edges = [tuple(edge.split()) for edge in edges.splitlines()]
    # for _ in edges:
    #     print(_)
    # graph = createGraph(edges)
    for edge in edges:
        if len(edge) == 3:
            has_weights = True
    if directed:
        graph = createDiGraph(edges)
        drawGraph(graph, directed)
    else:
        graph = createGraph(edges)
        drawGraph(graph, directed)

    st.sidebar.button("Nhập")

    st.sidebar.divider()

    st.sidebar.subheader("🪄Duyệt đồ thị:")
    startNode = st.sidebar.selectbox(
        "Chọn đỉnh bắt đầu:", options=list(graph.nodes()))
    traversalMethod = st.sidebar.selectbox(
        "Chọn phương thức duyệt:", options=["Duyệt theo chiều rộng (BFS)", "Duyệt theo chiều sâu (DFS)"])

    if st.sidebar.button("Duyệt"):
        if traversalMethod == "Duyệt theo chiều rộng (BFS)":
            bfs(graph, startNode)
        elif traversalMethod == "Duyệt theo chiều sâu (DFS)":
            dfs(graph, startNode)

    st.sidebar.divider()

    st.sidebar.subheader("🔃Kiểm tra tính liên thông:")
    st.sidebar.caption(
        "Sử dụng thuật toán :violet[Tarjan] - đếm số lượng bộ phận :red[Liên thông]/ :blue[Liên thông mạnh] của đồ thị :red[Vô hướng]/ :blue[Có hướng]")
    if st.sidebar.button("Kiểm tra"):
        strong_components = tarjan(graph)
        component_edges_list = []
        for component in strong_components:
            component_edges = get_component_edges(edges, component)
            component_edges_list.append(component_edges)
        if directed:
            st.subheader(
                f"Đồ thị có :blue[{len(component_edges_list)} bộ phận liên thông mạnh]")
            for i, component in enumerate(component_edges_list):
                st.text(f"Bộ phận liên thông mạnh {i+1}:")
                drawGraph(createDiGraph(component), directed)
        else:
            st.subheader(
                f"Đồ thị có :blue[{len(component_edges_list)} bộ phận liên thông]")
            for i, component in enumerate(component_edges_list):
                st.text(f"Bộ phận liên thông {i+1}:")
                drawGraph(createGraph(component), directed)
    st.sidebar.divider()
    st.sidebar.subheader("🤏Tìm đường đi ngắn nhất:")
    st.sidebar.caption(
        "Tìm đường đi ngắn nhất từ 1 đỉnh đến các đỉnh còn lại sử dụng thuật toán :violet[Moore-Dijkastra]")
    start_node = st.sidebar.selectbox('Chọn đỉnh nguồn:', graph.nodes)
    if st.sidebar.button("Tìm"):
        if has_weights:
            if start_node in graph.nodes:
                shortest_paths = bellman_ford(graph, start_node, edges)
                st.write(
                    f"Đường đi ngắn nhất từ đỉnh {start_node} đến tất cả các đỉnh khác là:")
                for node, distance in shortest_paths.items():
                    st.write(f"{start_node} -> {node}: {distance}")
        else:
            st.toast('Vui lòng nhập trọng số!', icon='⚠️')


if __name__ == "__main__":
    main()
