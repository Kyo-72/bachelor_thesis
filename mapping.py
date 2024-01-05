import copy

INF =10000

Q20_graph = [ [1,5],[0,2,6,7],[1,3,6,7],[2,4,8,9],[3,8,9],\
            [0,6,10,11],[1,2,5,7,10,11],[1,2,6,8,12,13],[3,4,7,9,12,13],\
            [3,4,8,14],[5,6,11,15],[5,6,10,12],\
            [7,8,11,13,16,17],[7,8,12,14,18,19],[9,13,18,19],[10,16],\
            [11,12,15,17],[11,12,16,18],[13,14,17,19],[13,14,18] ]
#key 指定ビット数　value (from,to) from node to bit　 0-index
mapping_node = {10:{0:0, 1:1, 2:2, 5:3, 6:4, 7:5, 10:6, 11:7, 12:8, 13:9}}

def create_adjacency_matrix(nodes):
    adjacency_matrix = [[ 0 for i in range(len(nodes)) ] for j in range(len(nodes))]
    for bit,node in enumerate(nodes):
        for to_bit in node:
            adjacency_matrix[bit][to_bit] = 1

    return adjacency_matrix

def warshall_floyd(matrix):
    n = len(matrix)
    #前処理 0をINFにかえる
    for i in range(n):
        for j in range(n):
            if(matrix[i][j] == 0 and i != j):
                matrix[i][j] = INF

    cost_matrix = copy.deepcopy(matrix)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                cost_matrix[i][j] = min(cost_matrix[i][j], cost_matrix[i][k] + cost_matrix[k][j])

    return cost_matrix

def find_out_path(start, end, matrix, cost_matrix):
    p = []
    n = len(matrix)
    curr = start
    while(curr != end):
        for k in range(n):
            if(k != curr and (matrix[curr][k] + cost_matrix[k][end] == cost_matrix[curr][end])):
                curr = k
                p.append(k)
                break

    return p

def map_graph(optimal_graph, nodes):

    mapped_bit = []
    # nna_graphの数をnode->q_bitに変換する
    for node in optimal_graph:
        mapped_bit.append([nodes[n] for n in node])

    return mapped_bit

def bit_mapping(bit_num):

    nodes = mapping_node[bit_num]

    nna_graph = []
    for node in nodes.keys():
        nna_graph.append(Q20_graph[node])

    used_node = [node for node in nodes.keys()]
    optimal_graph = []

    for node in nna_graph:
        #mapping_node[0]に含まれる数を排除する（つかわない）
        optimal_graph.append([adjacent_node for adjacent_node in node if adjacent_node in used_node])

    return map_graph(optimal_graph, nodes)

def virtual_mapping(trimed_node, link):

    optimal_graph = []
    for node in trimed_node.values():
        optimal_graph.append(node)

    return map_graph(optimal_graph, link)

matrix = create_adjacency_matrix(Q20_graph)
cost_matrix = warshall_floyd(matrix)
p = find_out_path(15, 8, matrix, cost_matrix)
print(p)