import copy
import mapping
import itertools
import heapq

NUM_OF_NODE = 20
MAX_COST    = 1000000

class bit_combination:

    def __init__(self, is_nna, necessary_node, usednode, is_added, num_node, num_combination):
        self.is_nna          = is_nna
        self.necessary_node  = necessary_node
        self.used_node       = usednode
        self.is_added        = is_added
        self.num_node        = num_node
        self.num_combination = num_combination

    def add_node(self, node):
        self.is_added  = True
        self.num_node += 1
        self.used_node += node 
    
    def nna(self):
        self.is_nna = True
        


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

#与えられたノード群が連結か判定する
def is_nna(used_node, node):
    trimmed_nodes = remove_unused_node(node, used_node)
    visited = [0 for i in range(NUM_OF_NODE)]
    start   = used_node[0]

    return compute_nna(trimmed_nodes, visited, start)

def compute_nna(trimed_node, visited, node):
    visited[node] = 1
    for v in trimed_node[node]:
        if(visited[v] == 0):
            compute_nna(trimed_node,visited, v)

    res = True

    for v in trimed_node.keys():
        if(visited[v] == 0):
            res = False

    return res

def compute_cost_of_bit_combination():
    pass

def evaluate_bit_combi(nna, used_node, num_combi, is_added):
    #ノード追加処理を行っていない組み合わせ場合
    if(is_added == False):
        res = {
            'is_nna'          : nna,            #nnaかどうか
            'necessary_node'  : used_node,      #必要なノード（ノード処理追加後）
            'used_node'       : used_node,      #もともとあるノード
            'is_added'        : False,          #ノード追加処理を行ったかどうか
            'num_node'        : len(used_node), #ノードの数
            'num_combination' : num_combi       #組み合わせ数
        }
    #ノード追加処理を行った組み合わせの場合
    else:
        pass

    return res

def calc_distance_on_graph(s, t, necessary_node,trimmed_node):
    visited    = {node:MAX_COST for node in necessary_node}
    visited[s] = 0

    hq = [(0, s)]
    heapq.heapify(hq)

    while(len(hq) > 0):
        present_node = heapq.heappop(hq)
        present_cost = present_node[0]

        for adjacent in trimmed_node[present_node[1]]:
            
            next_cost = present_cost + 1

            if(next_cost < visited[adjacent]):
                visited[adjacent] = next_cost
                heapq.heappush(hq, (next_cost, adjacent))

    return visited[t]

#グラフの中心性を計算
def compute_cost_for_combi(trimmed_node, used_node, add_nodes=[]):
    cost = 0
    necessary_node = used_node + list(add_nodes)
    
    for s in used_node:
        for t in used_node:
            if(t == s):
                continue
            cost += calc_distance_on_graph(s, t, necessary_node, trimmed_node)

    return cost


#bit_combinationを更新するとうまくいかない（続くやつが無理だから）
#この関数でforループ回さん方がよくね？組み合わせ一つに対してノードを探索する方が直感的では
def add_node_for_nna(node, bit_combination,max_num):
    for k,v in bit_combination.items():
        unused_node = [i for i in range(NUM_OF_NODE)]
        node_num = v['num_node']

        #すべてのノードと使われてるノードのbitXORを取って使ってないノードを求める
        unused_node = list(set(unused_node) ^ set(v['necessary_node']))

        #max_bitを超えないような追加ノードの選び方
        limit_addnode_num = max_num - node_num
        min_cost = MAX_COST

        #limig_addnode_numに達するまで、追加するノードの数を増やし、NNAを満たす組み合わせを探索する
        if(limit_addnode_num > 0):
            for m in range(limit_addnode_num + 1)[1:]:
                add_node_combi = list(itertools.combinations(unused_node, m))

                for add_nodes in add_node_combi:
                    necessary_node = v['used_node'] + list(add_nodes)
                    trimmed_node = remove_unused_node(node, necessary_node)

                    #検討しているノード群が連結ならコストを計算する
                    if(is_nna(necessary_node, node)):
                        #最小ならnecessary_setを更新
                        cost = compute_cost_for_combi(trimmed_node, v['used_node'], add_nodes)
                        if(min_cost > compute_cost_for_combi(trimmed_node, v['used_node'], add_nodes)):
                            min_cost = cost
                            v['necessary_node'] = v['used_node'] + list(add_nodes)
                            pass
        else:
            return []


def compute_handle_bits_combi(bit_set, node):
    bit_combination = {}
    n = len(bit_set)
    for bit in range(1 << n)[1: ]:
        used_node = []
        #組み合わせで使用するノードを計算
        for i in range(n):
            if(bit & (1 << i)):
                used_node = list(set(used_node) | set(bit_set[i]))
        
        nna = is_nna(used_node, node)
        num_combi = bin(bit).count('1')
        #ビットの組み合わせのクラスのインスタンスを作成\234
        bit_combination[bit] = evaluate_bit_combi(nna, used_node, num_combi, False)
                                
    return bit_combination

def find_optimal_combination(input, output, bit_set, node):
    bit_combination = compute_handle_bits_combi(bit_set, node)

def calc_cost(bit_combination):
    pass



node = [[1, 5], [0, 2, 6, 7], [1, 3, 6, 7], [0, 6, 10, 11], [1, 2, 5, 7, 10, 11], [1, 2, 6, 8, 12, 13], [5, 6, 11, 15], [5, 6, 10, 12], [7, 8, 11, 13, 16, 17], [7, 8, 12, 14, 18, 19]]
bit_set = [[0,1, 3],[0,1,2],[6,7,8]]
node = mapping.bit_mapping(10)

bit_combination = compute_handle_bits_combi(bit_set, node)
un_nna_combination = {}
for key,v in bit_combination.items():
    if(v['is_nna'] == False):
        un_nna_combination[key] = bit_combination[key]

add_node_for_nna(node, un_nna_combination,8)

pass
#TODO 
#全部falseの場合を考える
adopted_combi = []
max_score = 0
for combi in bit_combination.values():
    if(max_score < combi['num_combination']):
        max_score = combi['num_combination']
        adopted_combi = combi

pass
#全体に組み込む
#add_node_for_nnaの返り値を見て、無理な場合を考える

def solve_combination:
