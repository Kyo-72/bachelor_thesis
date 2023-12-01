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
        groups.append(group)

    return groups

nodes = [[1, 3], [0, 2, 4, 5], [1, 4, 5], [0, 4, 6, 7], [1, 2, 3, 5, 6, 7], [1, 2, 4, 8, 9], [3, 4, 7], [3, 4, 6, 8], [5, 7, 9], [5, 8]]
necessary_bit = [1, 2, 3, 6, 8, 9]
expect_count = 3
expect_groups = [[1, 2], [3, 6], [8, 9]]

groups = calc_groups(nodes, necessary_bit)
print(groups)