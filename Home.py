import streamlit as st 
import networkx as nx
import pyvis as pv
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd
from algo_lib.search import dfs, bfs, dfs_recursion
from algo_lib.scc import Tarjan
from algo_lib.shortest_path import bellman_ford
from algo_lib.topo import topo_sort
from algo_lib.mst import Kruskal, Prim


st.set_page_config(layout="centered",
                   page_title="GraphVify",
                   page_icon="🌐",
                   initial_sidebar_state="expanded")

# TẠO ĐỒ THỊ
# Vô hướng
def createGraph(edges):
    G = nx.Graph()
    for edge in edges:
        if len(edge) == 1:
            G.add_node(edge[0])
        elif len(edge) == 2:
            G.add_edge(edge[0], edge[1])
        elif len(edge) == 3:
            # lưu trữ trọng số cung bằng label
            # G.edges(data=True)
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
            G.add_edge(edge[0], edge[1], title=edge[2], label=edge[2])
        else:
            st.toast("Cung có nhiều hơn 4 tham số sẽ không hiển thị!", icon='⚠️')
    return G



# Vẽ đồ thị
def drawGraph(graph, directed):
    vis = Network(height="350px", width="100%", directed=directed)
    vis.from_nx(graph)
    vis.write_html("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=360)


def main():
    # Giao diện người dùng
    st.title("✨Graph:red[Vify]")
    with st.popover("Hướng dẫn 📎"):
        st.markdown("**Giới thiệu**\n\nỨng dụng web này cho phép bạn mô phỏng các thao tác cơ bản trên đồ thị, bao gồm:\n *   Nhập đồ thị\n*   Duyệt đồ thị\n*   Kiểm tra tính liên thông\n* Tìm đường đi ngắn nhất\n* Tìm cây khung nhỏ nhất\n\n **Hướng dẫn sử dụng**\n\n")
        with st.expander("Nhập đồ thị"):
            st.markdown("1.Chọn phương thức nhập **(Có hướng/ Vô hướng)**.\n\n 2.Nhập từng cặp đỉnh và trọng số (start end weight) của mỗi cạnh trên một dòng cách nhau bởi một khoảng trắng.\n\n 3.Nhấp vào nút **'Nhập'**.")
        with st.expander("Duyệt đồ thị"):
            st.markdown("1.Nhập đồ thị.\n\n2.Chọn đỉnh bắt đầu.\n\n3.Chọn thuật toán duyệt:\n\n*   Duyệt theo chiều sâu (DFS)\n*   Duyệt theo chiều rộng (BFS)\n\n4.Bấm nút **'Duyệt'**.\n\n5.Kết quả sẽ hiển thị trong bảng điều khiển.")
        with st.expander("Kiểm tra tính liên thông"):
            st.markdown("1.Nhập đồ thị.\n\n2.Nhấn nút **'Kiểm tra'**.\n\n3.Kết quả kiểm tra sẽ được hiển thị trong bảng điều khiển bao gồm:\n\n*   Số lượng bộ phân liên thông/ liên thông mạnh\n*   Các bộ phân liên thông/ liên thông mạnh")
        with st.expander("Tìm đường đi ngắn nhất"):
            st.markdown("1.Nhập đồ thị **(có trọng số)**.\n\n2.Chọn đỉnh nguồn.\n\n3.Nhấn nút **'Tìm'**.\n\n4.Kết quả sẽ được hiển thị trong bảng điều khiển dưới dạng:\n\n    A -> B : Đường đi ngắn nhất\n\nNếu kết quả trả về dạng:\n\n    A -> B : ♾️\n\n tức là không có đường đi từ A -> B.")
        with st.expander("Thứ tự Topo"):
            st.markdown("1.Nhập đồ thị **(có hướng không có chu trình)**.\n\n2.Nhấn nút **'Thực hiện'**.\n\n3.Kết quả sẽ được hiển thị trong bảng điều khiển.")
        with st.expander("Tìm cây khung nhỏ nhất"):
            st.markdown("1.Nhập đồ thị **(Có trọng số - Vô hướng - Liên thông)**.\n\n2.Chọn thuật toán:\n* Kruskal\n* Prim\n\n3.Nhấn nút **tìm cây khung**.\n\n4.Kết quả sẽ được hiển thị trong bảng điều khiển:\n* Cây khung nhỏ nhất\n* Trọng lượng")
    # Nhập danh sách cung

    # Nhập đồ thị
    st.sidebar.subheader("Nhập đồ thị:")
    directed = st.sidebar.toggle("Có hướng")
    edges = st.sidebar.text_area(
        "Danh sách cung (cạnh):", value="1 3 4\n3 2 5\n2 1 10\n5 6 2\n6 5 3\n3 5 1")
    edges = [edge.split() for edge in edges.splitlines()]
    # Vẽ đồ thị
    if directed:
        graph = createDiGraph(edges)
        with st.expander("Đồ thị", expanded=True):
            drawGraph(graph, directed)
    else:
        graph = createGraph(edges)
        with st.expander("Đồ thị", expanded=True):
            drawGraph(graph, directed)
    st.sidebar.button("Nhập")

    st.sidebar.divider()
    st.sidebar.subheader("Duyệt đồ thị:")
    start_node = st.sidebar.selectbox(
        "Chọn đỉnh bắt đầu:", options=list(graph.nodes()))
    traversalMethod = st.sidebar.selectbox(
        "Chọn phương thức duyệt:", options=["Duyệt theo chiều rộng (BFS)", "Duyệt theo chiều sâu (DFS)", "Duyệt theo chiều sâu (DFS Đệ quy)"])
    if st.sidebar.button("Duyệt"):
        if traversalMethod == "Duyệt theo chiều rộng (BFS)":
            st.markdown("<p>Thứ tự duyệt theo chiều rộng: </p>",unsafe_allow_html=True)
            for component in bfs(graph, start_node):
                st.subheader(' → '.join(component))
                st.divider()
        elif traversalMethod == "Duyệt theo chiều sâu (DFS)":
            st.markdown("<p>Thứ tự duyệt theo chiều sâu: </p>",unsafe_allow_html=True)
            for component in dfs(graph, start_node):
                st.subheader(' → '.join(component))
                st.divider()
        elif traversalMethod == "Duyệt theo chiều sâu (DFS Đệ quy)":
            st.markdown("<p>Thứ tự duyệt theo chiều sâu: </p>",unsafe_allow_html=True)
            for component in dfs_recursion(graph, start_node):
                st.subheader(' → '.join(component))
                st.divider()

    st.sidebar.divider()
    st.sidebar.subheader("Kiểm tra tính liên thông:")
    st.sidebar.caption(
        "Kiểm tra :red[tính liên thông] của đồ thị :blue[vô hướng]. \nDùng thuật toán :violet[Tarjan] đếm số lượng bộ phận :red[liên thông mạnh] của đồ thị :blue[có hướng].")
    if st.sidebar.button("Kiểm tra"):
        if directed:
            scc = Tarjan(graph)
            print(scc)
            st.subheader(f"Đồ thị có :blue[{len(scc)} bộ phận liên thông mạnh]")
            for i, component in enumerate(scc):
                component_graph = graph.copy()
                component_graph.remove_nodes_from(set(graph.nodes)-set(component))
                st.text(f"Bộ phận liên thông mạnh {i+1}:")
                drawGraph(component_graph, directed)
        else:
            list_component  = bfs(graph, start_node)
            if len(list_component) == 1:
                st.subheader(":blue[Đồ thị có tính liên thông!]")
                drawGraph(graph, directed)
            else:
                st.subheader(":red[Đồ thị không liên thông!]")
                for i, component in enumerate(list_component):
                    st.text(f"Bộ phận liên thông {i+1}:")
                    component_graph = graph.copy()
                    component_graph.remove_nodes_from(set(graph.nodes)-set(component))
                    drawGraph(component_graph, directed)
    # CẬP NHẬT ĐẾN ĐÂY                 
    st.sidebar.divider()
    st.sidebar.subheader("Tìm đường đi ngắn nhất:")
    st.sidebar.caption(
        "Tìm đường đi ngắn nhất từ 1 đỉnh đến các đỉnh còn lại sử dụng thuật toán :violet[Bellman Ford]")
    start_node = st.sidebar.selectbox('Chọn đỉnh nguồn:', graph.nodes)
    if st.sidebar.button("Tìm"):
        if all(len(edge)==3 for edge in edges):
            if start_node in graph.nodes:
                shortest_paths = bellman_ford(graph, start_node, edges)
                with st.expander(f"Đường đi ngắn nhất từ đỉnh :blue[{start_node}] đến tất cả các đỉnh khác là:"):
                    for node, distance in shortest_paths.items():
                        if (distance != float('inf')):
                            st.subheader(f"{start_node} -> {node}: {distance}")
                        else:
                            st.subheader(f"{start_node} -> {node}: ♾️")
        else:
            st.toast('Vui lòng nhập trọng số!', icon='⚠️')

    st.sidebar.divider()
    st.sidebar.subheader("Thứ tự topo:")
    st.sidebar.caption(
        "Xếp các đỉnh của đồ thị :red[có hướng không có chu trình (DAG)] theo thứ tự topo")
    if st.sidebar.button("Thực hiện"):
        if directed:
            try:
                topo_order = []
                topo_sort(graph, topo_order, edges)
            except:
                st.toast(
                    'Đồ thị không phải là DAG, không thể tính toán thứ tự topo.', icon='⚠️')
                return
            # st.table(pd.DataFrame(topo_order, columns=['Đỉnh']).T)
            
            st.subheader('Thứ tự topo: '+', '.join(topo_order))
        else:
            st.toast('Đồ thị vô hướng không thể tính toán thứ tự topo!', icon='⚠️')
    
    st.sidebar.divider()
    st.sidebar.subheader("Tìm cây khung nhỏ nhất:")
    st.sidebar.caption("Sử dụng thuật toán :violet[Kruskal] hoặc :violet[Prim] để tìm cây khung nhỏ nhất")
    mst_algo = st.sidebar.selectbox("Chọn thuật toán:", options=["Kruskal", "Prim"])
    if mst_algo == "Prim":
        start_node_Prim = st.sidebar.selectbox("Chọn đỉnh bắt đầu tìm:", options=list(graph.nodes()))
    if st.sidebar.button("Tìm cây khung"):
        if directed:
            st.toast('Đồ thị có hướng không thể tìm cây khung nhỏ nhất!', icon='⚠️')
        elif len(bfs(graph, list(graph.nodes)[0])) != len(graph.nodes):
            st.toast("Đồ thị không liên thông không thể tìm cây khung nhỏ nhất!", icon='⚠️')
        elif not all(len(edge) == 3 for edge in edges) :
            st.toast("Vui lòng nhập trọng số cho tất cả cung!", icon='⚠️')
        else:
            if mst_algo == "Kruskal":
                mst = Kruskal(graph)
            elif mst_algo == "Prim":
                mst = Prim(graph, start_node_Prim)
            
            mst_graph = createGraph(mst[0])

            
            st.subheader("Cây khung nhỏ nhất")
            drawGraph(mst_graph, directed)
            st.subheader(f"Trọng lượng: {mst[1]}")
    # lst={node : float(node) for node in graph.nodes}
    # lst.sort(reverse=False)
    # print(lst)
    # print(type(lst[0]))
    # print(list(set(graph.nodes)-set(['1','2'])))

            # print(mst)
            # print(mst_graph)
            with st.expander("🌲Cây khung nhỏ nhất"):
            # st.subheader("Cây khung nhỏ nhất")
                drawGraph(mst_graph, directed)
                st.markdown(f"Trọng lượng: **:green[{mst[1]}]**")
    # edges = ['3','2','1']
    # edges.sort(reverse=False)
    # print(edges)


if __name__ == "__main__":
    main()
