Q20_graph = [ [1,5],[0,2,6,7],[1,3,6,7],[2,4,8,9],[3,8,9],\
             [0,6,10,11],[1,2,5,7,10,11],[1,2,6,8,12,13],[3,4,7,9,12,13],\
             [3,4,8,14],[5,6,11,15],[5,6,10,12],\
             [7,8,11,13,16,17],[7,8,12,14,18,19],[9,13,18,19],[10,16],\
             [11,12,15,17],[11,12,16,18],[13,14,17,19],[13,14,18] ]
#key 指定ビット数　value (from,to) from node to bit　
mapping_node = {10:{1:1, 2:2, 3:3, 6:4, 7:5, 8:6, 11:7, 12:8, 13:9, 14:10}}

def calc_optimal_graph(nodes):
    nna_graph = []
    for node in nodes.keys():
        nna_graph.append(Q20_graph[node - 1])

    used_node = [(node - 1) for node in nodes.keys()]
    optimal_graph = []
    for node in nna_graph:
        #mapping_node[0]に含まれる数を排除する（つかわない）
        optimal_graph.append([adjacent_node for adjacent_node in node if adjacent_node in used_node])
    
    mapped_bit = []
    #TODO nna_graphの数をnode->q_bitに変換する
    for node in optimal_graph:
        mapped_bit.append([nodes[n + 1] for n in node])

    return nna_graph