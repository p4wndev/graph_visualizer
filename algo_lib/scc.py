def Tarjan(graph):
    scc = []
    k = 1
    min_num = {}
    num = {}
    stack = []

    def SCC(graph, u, k):
        num[u] = k
        min_num[u] = k
        k = k + 1
        stack.append(u)

        neighbors = [int(node) for node in graph.neighbors(u)]
        neighbors.sort(reverse=False)
        for v in neighbors:
            if str(v) not in num:
                SCC(graph, str(v), k)
                min_num[u] = min(min_num[u], min_num[str(v)])
            elif str(v) in stack:
                min_num[u] = min(min_num[u], min_num[str(v)])

        if num[u] == min_num[u]:
            component = []
            while True:
                w = stack.pop()
                component.append(w)
                if w == u:
                    break
            scc.append(component)
    
    nodes = [int(node) for node in graph.nodes]
    nodes.sort(reverse=False)
    for node in nodes:
        if str(node) not in num:
            SCC(graph, str(node), k)

    return scc
