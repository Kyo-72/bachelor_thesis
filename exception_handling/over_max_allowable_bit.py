import sys
import copy
sys.path.append('/Users/kyo72/Program/lab/m2')

import const
import display
from solve_combination import remove_unused_node
from graph.groups import calc_groups
from generate_circuit_by_bitset import generate_circuit
from sabreSWAP import insert_swap_by_sabre

def convert_dici_to_circuit(circuit_list, n):
    circuit = [[const.EMPTY for i in range(n)] for j in range(len(circuit_list))]
    circuit_list.reverse()
    for d, gate in enumerate(circuit_list):
        target_bit   = gate[0]
        controll_bit = gate[1]
        circuit[d][target_bit] = const.TARGET_BIT
        circuit[d][controll_bit] = const.CONTROLL_BIT

    return circuit


def one_group_circuit(nodes, used_node, init_node=None):
    #[[0,1], [0、2] qubit0->qubit1 qubit0->qubit2へのCNOT(qubit0がターゲットビット)
    circuit_list = []
    visited = []
    #中央値をしない場合、適当な位置を設定
    if(init_node == None):
        visited.append(used_node[0])

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

def two_group_circuit(node, bit_set, n):
    circuit = generate_circuit(bit_set, n)

    return insert_swap_by_sabre(circuit, node)

def handling_over_bit_circuit(node, necessary_node, n):
    groups     = calc_groups(node, copy.copy(necessary_node))
    group_size = len(groups)
    used_node = remove_unused_node(node, necessary_node)

    circuit_list = []
    circuit = []

    #グループが1時の処理
    if(group_size == 1):
        circuit_list = one_group_circuit(used_node, necessary_node)
        circuit = convert_dici_to_circuit(circuit_list, n)
    elif(group_size >= 2):
        circuit = two_group_circuit(node, necessary_node, n)
        print('--------------------------------')
        print(circuit)
        print('--------------------------------')

    return circuit


