def calc_neighbor_node(node, necessary_bit, not_calclated_nodes, group, state):
    for n in node[state]:
        #指定したノードが探索済みなら飛ばす
        if(n not in not_calclated_nodes):
            continue

        #探索したノードを削除
        not_calclated_nodes.remove(n)
        state = n
        group.append(n)

        calc_neighbor_node(node, necessary_bit, not_calclated_nodes, group, state)

def calc_groups(nodes, necessary_bit):
    not_calclated_nodes = necessary_bit
    groups = []
    #すべてのnecessary_bitがどのグループに属するか求める
    while( len( necessary_bit ) != 0 ):
        start_node = necessary_bit[0]
        group = []
        calc_neighbor_node(nodes, necessary_bit, not_calclated_nodes, group, start_node)
        #隣接するノードがなければ，探索するノードを次に進める
        if(group == []):
            groups.append([start_node])
            not_calclated_nodes.remove(start_node)
        else:
            groups.append(group)

    return groups

