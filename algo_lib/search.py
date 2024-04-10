def bfs(graph, start_node):
    components = []
    def BFS(graph, start_node):
        visited = set()
        queue = [start_node]
        order = []
        
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            neighbors = [int(node) for node in graph.neighbors(node)]
            neighbors.sort(reverse=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(str(neighbor))
        components.append(order)
        return visited
    # duyệt toàn bộ đồ thị
    nodes = set(graph.nodes) - BFS(graph, start_node)
    while nodes:
        lst = [int(node) for node in nodes]
        lst.sort()
        nodes = nodes - BFS(graph, str(lst[0]))
    return components

def dfs(graph, start_node):
    components = []
    def DFS(graph, start_node):
        visited = set()
        stack = [start_node]
        order = []
        
        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)
            neighbors = [int(node) for node in graph.neighbors(node)]
            neighbors.sort(reverse=False)
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(str(neighbor))
        components.append(order)
        return visited
    # duyệt toàn bộ đồ thị
    nodes = set(graph.nodes)-DFS(graph, start_node)
    while nodes:
        lst = list(nodes)
        lst.sort()
        nodes = nodes-DFS(graph, lst[0])
    return components

def dfs_recursion(graph, start_node):
    visited = set()
    components = []
    def DFS(graph, start_node):
        order = []
        def recursion(node):
            visited.add(node)
            order.append(node)
            neighbors = [int(node) for node in graph.neighbors(node)]
            neighbors.sort(reverse=False)
            for neighbor in neighbors:
                if str(neighbor) not in visited:
                    recursion(str(neighbor))
        recursion(start_node)
        components.append(order)
        return visited
     # duyệt toàn bộ đồ thị
    nodes = set(graph.nodes)-DFS(graph, start_node)
    while nodes:
        lst = list(nodes)
        lst.sort()
        nodes = nodes-DFS(graph, lst[0])
    return components

'''
Test case:
13 15
1 4
1 2
1 12
2 4
3 7
4 6
4 7
5 8
5 9
6 7
6 13
8 9
10 11
10 12
11 12
'''
