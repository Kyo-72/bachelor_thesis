import sys
import copy

sys.path.append('/Users/kyo72/Program/lab/m2')

import const
import display
from solve_combination import remove_unused_node
from graph.groups import calc_groups

def convert_dici_to_circuit(circuit_list, n):
    circuit = [[const.EMPTY for i in range(n)] for j in range(len(circuit_list))]
    circuit_list.reverse()
    for d, gate in enumerate(circuit_list):
        target_bit   = gate[0]
        controll_bit = gate[1]
        circuit[d][target_bit] = const.TARGET_BIT
        circuit[d][controll_bit] = const.CONTROLL_BIT

    return circuit


def one_group_circuit(nodes, used_node):
    #[[0,1], [0、2] qubit0->qubit1 qubit0->qubit2へのCNOT(qubit0がターゲットビット)
    circuit_list = []
    visited = [used_node[0]]
    queue = [copy.copy(used_node[0])]
    while( len(queue) != 0 ):
        node = queue.pop()
        for adjacend_node in nodes[node]:
            #探索済みノードを二度探索しないため
            if(adjacend_node in visited):
                continue

            visited.append(adjacend_node)
            queue.append(adjacend_node)
            circuit_list.append([node, adjacend_node])

    return circuit_list


def handling_over_bit_circuit(node, necessary_node, n):
    groups     = calc_groups(node, copy.copy(necessary_node))
    group_size = len(groups)
    used_node = remove_unused_node(node, necessary_node)

    circuit_list = []

    #グループが1だった時の処理
    if(group_size == 1):
        circuit_list = one_group_circuit(used_node, necessary_node)
    else:
        pass

    circuit = convert_dici_to_circuit(circuit_list, n)
    display.display_circuit(circuit, [0,1,2,3,4,5,6,7,8,9,])
    print(circuit_list)


n = 10
nodes = [[1, 3], [0, 2, 4, 5], [1, 4, 5], [0, 4, 6, 7], [1, 2, 3, 5, 6, 7], [1, 2, 4, 8, 9], [3, 4, 7], [3, 4, 6, 8], [5, 7, 9], [5, 8]]
combi = {'is_nna': True, 'necessary_node': [2, 3, 5, 6, 7, 8, 9], 'used_node': [0, 3, 5, 7], 'is_added': False, 'num_node': 6, 'num_combination': 1, 'select_combi': [0], 'select_combi_bit': 1}

handling_over_bit_circuit(nodes, combi['necessary_node'], n)


