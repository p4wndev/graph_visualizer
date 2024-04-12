import streamlit as st 
import networkx as nx
import pyvis as pv
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd
from algo_lib.search import dfs, bfs, dfs_recursion
from algo_lib.scc import Tarjan
from algo_lib.shortest_path import Moore_Dijkstra, Bellman_Ford, Floyd_Warshall, negative_weight_cycle
from algo_lib.topo import topo_sort, rank
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
            G.add_edge(edge[0], edge[1], title='', label='')
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
            G.add_edge(edge[0], edge[1], title='', label='')
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

    # Nhập đồ thị
    st.sidebar.subheader("Nhập đồ thị:")
    directed = st.sidebar.radio("Loại đồ thị:",options=[":blue[Vô hướng]", ":red[Có hướng]"])
    directed = (directed == ":red[Có hướng]")
    edges = st.sidebar.text_area(
        "Danh sách cung (cạnh):", value="1 3 4\n3 2 5\n2 1 10\n5 6 2\n6 5 3\n3 5 1")
    st.sidebar.button("Nhập")
    # Vẽ đồ thị
    edges = [edge.split() for edge in edges.splitlines()]
    graph = createDiGraph(edges) if directed else createGraph(edges)
    with st.expander("Đồ thị", expanded=True):
        drawGraph(graph, directed)
    
    nodes = [int(node) for node in graph.nodes]
    nodes.sort(reverse=False)
    nodes = [str(node) for node in nodes]

    # Duyệt đồ thị
    st.sidebar.divider()
    st.sidebar.subheader("Duyệt đồ thị:")
    startNode = st.sidebar.selectbox(
        "Chọn đỉnh bắt đầu duyệt:", options = nodes)
    traversalMethod = st.sidebar.selectbox(
        "Chọn phương thức duyệt:", options=["Duyệt theo chiều rộng (BFS)", "Duyệt theo chiều sâu (DFS)", "Duyệt theo chiều sâu (DFS Đệ quy)"])
    if st.sidebar.button("Duyệt"):
        if traversalMethod == "Duyệt theo chiều rộng (BFS)":
            st.markdown("<p>Thứ tự duyệt theo chiều rộng: </p>",unsafe_allow_html=True)
            for component in bfs(graph, startNode):
                st.subheader(' → '.join(component))
                st.divider()
        elif traversalMethod == "Duyệt theo chiều sâu (DFS)":
            st.markdown("<p>Thứ tự duyệt theo chiều sâu: </p>",unsafe_allow_html=True)
            for component in dfs(graph, startNode):
                st.subheader(' → '.join(component))
                st.divider()
        elif traversalMethod == "Duyệt theo chiều sâu (DFS Đệ quy)":
            st.markdown("<p>Thứ tự duyệt theo chiều sâu: </p>",unsafe_allow_html=True)
            for component in dfs_recursion(graph, startNode):
                st.subheader(' → '.join(component))
                st.divider()
    # Kiểm tra tính liên thông
    st.sidebar.divider()
    st.sidebar.subheader("Kiểm tra tính liên thông:")
    st.sidebar.caption(
        "Kiểm tra tính :blue[liên thông]/:red[liên thông mạnh] của đồ thị :blue[vô hướng]/:red[có hướng]")
    if st.sidebar.button("Kiểm tra"):
        if directed:
            scc = Tarjan(graph)
            if len(scc) == 1:
                st.subheader(":blue[Đồ thị liên thông mạnh!]")
                drawGraph(graph, directed)
            else:
                st.subheader(":red[Đồ thị không liên thông mạnh!]")
                st.subheader(f":blue[Đồ thị có {len(scc)} bộ phận liên thông mạnh]")
                for i, component in enumerate(scc):
                    component_graph = graph.copy()
                    component_graph.remove_nodes_from(set(nodes)-set(component))
                    st.text(f"Bộ phận liên thông mạnh {i+1}:")
                    drawGraph(component_graph, directed)
        else:
            list_component  = bfs(graph, startNode)
            if len(list_component) == 1:
                st.subheader(":blue[Đồ thị liên thông!]")
                drawGraph(graph, directed)
            else:
                st.subheader(":red[Đồ thị không liên thông!]")
                st.subheader(f":blue[Đồ thị có {len(list_component)} bộ phận liên thông]")
                for i, component in enumerate(list_component):
                    st.text(f"Bộ phận liên thông {i+1}:")
                    component_graph = graph.copy()
                    component_graph.remove_nodes_from(set(nodes)-set(component))
                    drawGraph(component_graph, directed)
    # Tìm đường đi ngắn nhất
    st.sidebar.divider()
    st.sidebar.subheader("Tìm đường đi ngắn nhất:")
    st.sidebar.caption("Tìm đường đi ngắn nhất sử dụng thuật toán :violet[Moore-Dijkstra], :violet[Bellman-Ford] hoặc :violet[Floyd-Warshall]")
    shortest_paths_algo = st.sidebar.selectbox('Chọn thuật toán:', ['Moore-Dijkstra', 'Bellman-Ford', 'Floyd-Warshall'])
    ways_to_search = st.sidebar.selectbox('Tìm đường đi ngắn nhất', ['Từ 1 đỉnh đến các đỉnh còn lại', 'Giữa 2 đỉnh'])
    start_node = st.sidebar.selectbox('Chọn đỉnh đầu:', options = nodes)
    if ways_to_search == 'Giữa 2 đỉnh':
        finish_node = st.sidebar.selectbox('Chọn đỉnh cuối:', options = nodes)
    if st.sidebar.button("Tìm"):
        # -------------- #
        def _2node_(path_graph, finish_node):
            if path_graph[1] == float('inf'):
                str_ps = f":red[Không có đường đi] từ đỉnh :blue[{start_node}] đến đỉnh :blue[{finish_node}]"
            else:
                str_ps = f"Đường đi ngắn nhất từ đỉnh :blue[{start_node}] đến đỉnh :blue[{finish_node}] là: :red[{path_graph[1]}]"
            with st.expander(str_ps):
                drawGraph(path_graph[0], directed)
        # -------------- #
        if not all(graph.get_edge_data(edge[0], edge[1])['label'] != '' for edge in graph.edges):
            st.toast('Vui lòng nhập trọng số!', icon='⚠️')
        # Moore-Dijkstra
        elif shortest_paths_algo == 'Moore-Dijkstra':
            if not all(float(graph.get_edge_data(edge[0],edge[1])['label']) >= 0 for edge in graph.edges):
                st.toast("Moore-Dijkstra chỉ áp dụng cho đồ thị có trọng số không âm!", icon='⚠️')
            elif ways_to_search == 'Giữa 2 đỉnh':
                _2node_(Moore_Dijkstra(graph, start_node, finish_node), finish_node)
            else:
                st.subheader(f"Đường đi ngắn nhất từ đỉnh :blue[{start_node}] đến tất cả các đỉnh là:")
                for node in nodes:
                    _2node_(Moore_Dijkstra(graph, start_node, node), finish_node=node)
        # Bellman-Ford
        elif shortest_paths_algo == 'Bellman-Ford':
            if negative_weight_cycle(graph, start_node, 'Bellman_Ford'):
                st.toast("Đồ thị chứa chu trình trọng số âm!", icon='⚠️')
            elif ways_to_search == 'Giữa 2 đỉnh':
                _2node_(Bellman_Ford(graph, start_node, finish_node), finish_node)
            else:
                st.subheader(f"Đường đi ngắn nhất từ đỉnh :blue[{start_node}] đến tất cả các đỉnh là:")
                for finish_node in nodes:
                    _2node_(Bellman_Ford(graph, start_node, finish_node), finish_node)
        # Floyd-Warshall
        elif shortest_paths_algo == 'Floyd-Warshall':
            if negative_weight_cycle(graph, start_node, 'Floyd_Warshall'):
                st.toast("Đồ thị chứa chu trình trọng số âm!", icon='⚠️')
            elif ways_to_search == 'Giữa 2 đỉnh':
                _2node_(Floyd_Warshall(graph, start_node, finish_node), finish_node)
            else:
                st.subheader(f"Đường đi ngắn nhất từ đỉnh :blue[{start_node}] đến tất cả các đỉnh là:")
                for finish_node in nodes:
                    _2node_(Floyd_Warshall(graph, start_node, finish_node), finish_node)       
    # Thứ tự topo 
    st.sidebar.divider()
    st.sidebar.subheader("Thứ tự topo:")
    st.sidebar.caption("Sắp xếp các đỉnh của đồ thị :red[có hướng không có chu trình (DAG)] theo thứ tự topo")
    if st.sidebar.button("Sắp xếp"):
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
    # Xếp hạng đồ thị 
    st.sidebar.divider()
    st.sidebar.subheader("Xếp hạng đồ thị:")
    st.sidebar.caption("Ứng dụng :violet[sắp xếp topo] xếp hạng các đỉnh của đồ thị")
    if st.sidebar.button("Xếp hạng"):
        if directed:
            if topo_sort(graph)[1]:#Kiểm tra đồ thị có chứa chu trình hay không
                rank_topo = rank(graph)
                for i, rank_num in enumerate(rank_topo):
                    with st.expander(f"Hạng {i+1}"):
                        st.subheader(', '.join(rank_num))
            else:
                st.toast('Đồ thị chứa chu trình, không thể xếp hạng!', icon='⚠️')
        else:
            st.toast('Đồ thị vô hướng không thể xếp hạng!', icon='⚠️')
        
    #------------------------------------------------
    
    # '''CÂY KHUNG'''
    
    #------------------------------------------------
    
    st.sidebar.divider()
    st.sidebar.subheader("Luồng cực đại:")
    st.sidebar.caption("Tìm luồng cực đại trong mạng bằng thuật toán đánh dấu :violet[Ford-Fulkerson]")
    if st.sidebar.button(":grey[Tìm]"):
        if directed:
            if topo_sort(graph)[1]:#Kiểm tra đồ thị có chứa chu trình hay không
                rank_topo = rank(graph)
                is_network = len(rank_topo[0])==1 and len(rank_topo[-1])==1
                if is_network:# Kiểm tra đồ thị có phải mạng hay không
                    max_flow = Ford_Fulkerson(graph, rank_topo[0][0], rank_topo[-1][0])
                    max_flow_graph = graph.copy()
                    S, T = max_flow[0], max_flow[1]
                    for s in S:
                        for t in T:
                            if graph.has_edge(s, t):
                                max_flow_graph.add_edge(s, t, color='red')
                    st.subheader(f":blue[Luồng cực đại trong mạng] = :red[{max_flow[-1]}]")
                    drawGraph(max_flow_graph, directed)
                else:
                    st.toast('Đồ thị không phải mạng, không thể tìm luồng cực đại!', icon='⚠️')
            else:
                st.toast('Đồ thị chứa chu trình, không thể tìm luồng cực đại!', icon='⚠️')
          else:
              st.toast('Đồ thị có hướng không thể tìm cây khung nhỏ nhất!', icon='⚠️')
          elif len(bfs(graph, nodes)[0]) != len(nodes):
              st.toast("Đồ thị không liên thông không thể tìm cây khung nhỏ nhất!", icon='⚠️')
          elif not all(len(edge) == 3 for edge in edges) :
              st.toast("Vui lòng nhập trọng số cho tất cả cung!", icon='⚠️')

if __name__ == "__main__":
    main()
