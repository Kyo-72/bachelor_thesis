import copy
import mapping

NUM_OF_NODE = 20

def create_adjacency_matrix(nodes):
    adjacency_matrix = [[ 0 for i in range(len(nodes)) ] for j in range(len(nodes))]
    for bit,node in enumerate(nodes):
        for to_bit in node:
            adjacency_matrix[bit][to_bit] = 1

    return adjacency_matrix        

def remove_unused_node(nodes,used_node):
    used_node = {bit:[] for bit in used_node}
    for bit,adjacent_list in enumerate(nodes):
        if(bit not in used_node):
                continue
        for to_bit in adjacent_list:
            if(to_bit not in used_node):
                continue;
            used_node[bit].append(to_bit)

    return used_node

def is_nna(trimed_node, visited, node):
    visited[node] = 1
    for v in trimed_node[node]:
        if(visited[v] == 0):
            is_nna(trimed_node,visited,v)

    res = True

    for v in trimed_node.keys():
        if(visited[v] == 0):
            res = False

    return res

def add_node_for_nna(node, bit_combination):
    pass


def bit_search(input, bit_set, node):
    cost = 0
    n = len(input)
    for bit in range(1 << n):
        pass


    return bit_combination

def compute_combination_cost(bit_set, node):
    bit_combination = {}
    n = len(bit_set)
    for bit in range(1 << n)[1: ]:
        used_node = []
        #組み合わせで使用するノードを計算
        for i in range(n):
            if(bit & (1 << i)):
                used_node = list(set(used_node) | set(bit_set[i]))

        node_num = len(used_node)
        trimmed_nodes = remove_unused_node(node, used_node)
        visited = [0 for i in range(NUM_OF_NODE)]
        num_combi = bin(bit).count('1')
        nna = is_nna(trimmed_nodes, visited , used_node[0])
        
        bit_combination[bit] = {'is_nna' : nna,
                                'used_node': used_node,
                                'num_node' : len(used_node),
                                'num_combination' : num_combi}
        
    return bit_combination

def find_optimal_combination(input, output, bit_set, node):
    bit_combination = compute_combination_cost(bit_set, node, visited=None)





node = [[1, 5], [0, 2, 6, 7], [1, 3, 6, 7], [0, 6, 10, 11], [1, 2, 5, 7, 10, 11], [1, 2, 6, 8, 12, 13], [5, 6, 11, 15], [5, 6, 10, 12], [7, 8, 11, 13, 16, 17], [7, 8, 12, 14, 18, 19]]
bit_set = [[0,1, 3],[0,1,2],[6,7,8]]
node = mapping.bit_mapping(10)

bit_combination = compute_combination_cost(bit_set, node)
pass