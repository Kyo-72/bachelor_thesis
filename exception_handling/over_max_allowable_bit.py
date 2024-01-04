import sys
import copy
sys.path.append('/Users/kyo72/Program/lab/m2')

from solve_combination import remove_unused_node
from graph.groups import calc_groups
#TODO ノードの中心に向けてCNOTゲートを配置する

def one_group_circuit(nodes, used_node):
    #[{0:1}{0:2}] qubit0->qubit1 qubit0->qubit2へのCNOT(qubit0がターゲットビット)
    circuit = []
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
            circuit.append({node:adjacend_node})

    return circuit


def handling_over_bit_circuit(node, necessary_node):
    groups     = calc_groups(node, copy.copy(necessary_node))
    group_size = len(groups)
    used_node = remove_unused_node(node, necessary_node)

    circuit = []

    #グループが1だった時の処理
    if(group_size == 1):
        circuit = one_group_circuit(used_node, necessary_node)
    else:
        pass

    print(circuit)

nodes = [[1, 3], [0, 2, 4, 5], [1, 4, 5], [0, 4, 6, 7], [1, 2, 3, 5, 6, 7], [1, 2, 4, 8, 9], [3, 4, 7], [3, 4, 6, 8], [5, 7, 9], [5, 8]]
combi = {'is_nna': True, 'necessary_node': [2, 3, 5, 6, 7, 8, 9], 'used_node': [0, 3, 5, 7], 'is_added': False, 'num_node': 6, 'num_combination': 1, 'select_combi': [0], 'select_combi_bit': 1}

handling_over_bit_circuit(nodes, combi['necessary_node'])


