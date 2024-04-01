# KIỂM TRA BỘ PHẬN LIÊN THÔNG
def Tarjan(graph):
    k = 1
    min_num = {}
    num = {}
    stack = []
    strong_components = []

    def SCC(graph, start_node, k):
        num.update({start_node: k})
        min_num.update({start_node: k})
        k = k+1
        stack.append(start_node)

        for v in graph.neighbors(start_node):
            if v not in num:
                SCC(graph, v, k)
                min_num.update(
                    {start_node: min(min_num.get(start_node), min_num.get(v))})
            elif v in stack:
                min_num.update(
                    {start_node: min(min_num.get(start_node), num.get(v))})

        if num.get(start_node) == min_num.get(start_node):
            component = []
            while True:
                w = stack.pop()
                component.append(w)
                if w == start_node:
                    break
            if len(component) != 0:
                strong_components.append(component)

    for node in list(graph.nodes):
        if node not in num:
            SCC(graph, node, k)
    return strong_components
