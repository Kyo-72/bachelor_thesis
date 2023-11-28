from pickletools import optimize
from re import A
from z3 import *
import const
from desired_output import desired_output
import display
import solve_combination
import copy
import mapping
import place_elementary_gate

MAX_NUM_GATE = 20

Q20_graph = [ [1,5],[0,2,6,7],[1,3,6,7],[2,4,8,9],[3,8,9],\
            [0,6,10,11],[1,2,5,7,10,11],[1,2,6,8,12,13],[3,4,7,9,12,13],\
            [3,4,8,14],[5,6,11,15],[5,6,10,12],\
            [7,8,11,13,16,17],[7,8,12,14,18,19],[9,13,18,19],[10,16],\
            [11,12,15,17],[11,12,16,18],[13,14,17,19],[13,14,18] ]

Optimized_nodes = []

def nearest_neighbor(n, s, node):

    #使わないノードの情報を無くす(indexエラーを避ける)
    for list in node:
        if(type(list) is int):
            break
        delete = []
        tmp = []
        for i in list:
            if(i < n):
                tmp.append(i)

        Optimized_nodes.append(tmp)

def one_bit_per_gate(vec, n, s):

    P_vec = [Bool("P_vec%d" % i) for i in range(n)]

    for i in range(n):
        P_vec[i] = vec[i]
        for j in range(n):
            if(i != j):
                P_vec[i] = And(P_vec[i],Not(vec[j]))

    #全ての制約をorで追加したい
    P = P_vec[0]
    for i in range(1,n):
        P = Or(P,P_vec[i])

    s.add(P)

def generate_output(f_vec, c_vec, t_vec, d, n, node):

    for d in range(d):
        for i in range(n):
            f_vec[d + 1][i] = f_vec[d][i]
            for j in range(n):
                #iがターゲットビット、jがコントロールビット
                #コントロールビットとターゲットビットが隣接していれば制約を追加
                if(i != j and i in node[j]):
                    f_vec[d + 1][i] = If(And(t_vec[d][i],c_vec[d][j]),f_vec[d + 1][i]^f_vec[d][j],f_vec[d + 1][i])

def equal_desired_output(f_vec, desired_output, n, d, s, H_gate_vec, T_gate_vec, T_dagger_gate_vec):

    i = 0
    for output in desired_output:

        P = False
        output_function = abs(output[0])
        gate_tyep = output[1]

        #Hゲートなら部分回路の終端の論理関数だけに着目
        if(gate_tyep == const.HADAMARD_GATE):
            for i in range(n):
                P = Or(P, f_vec[d][i] == output_function)
                H_gate_vec[d][i] = (f_vec[d][i] == output_function);

        #Tゲート以外なら部分回路の任意の場所に配置可能
        else:

            for i in range(d + 1):
                for j in range(n):
                    #括弧ないがそのままゲート変数になる
                    P = Or(P,(f_vec[i][j] == output_function) )
                    if(gate_tyep == const.T_GATE):
                        T_gate_vec[i][j] = (f_vec[i][j] == output_function)
                    elif(gate_tyep == const.T_DAGGER_GATE):
                        T_dagger_gate_vec[i][j] = (f_vec[i][j] == output_function)

        s.add(P)

def ex_equal_desired_output(f_vec,output_list,n,d,s):
    #負の数の処理
    for i in range(len(output_list)):
        output_list[i] = abs(output_list[i])

    for output in output_list:

        #要求出力と出力が正しいかを判定
        s.add(f_vec[d][output_list.index(output)] == output)

def display_bool(c_vec,t_vec,m,d,n):

    for i in range(d):
        for j in range(n):

            print("%d個目、%dライン"%(i+1,j))
            print("%s"%is_true( m[ c_vec[i][j] ] ))
            print("%s"%is_true( m[ t_vec[i][j] ] ))
        print()

def convert_output(m,d,n,c_vec,t_vec):
    output = [[" " for j in range(n)] for i in range(d)]

    for i in range(d):
        output
        for j in range(n):
            if(m[c_vec[i][j]] == True):
                output[i][j] = "c"

            if(m[t_vec[i][j]] == True):
                output[i][j] = "t"

    return output

#i ~ d + 1 j ~ nまでの not T_gate_vec[i][j]をAndでつなげた論理式を生成
def generate_restriction_of_other_gate_position(T_gate_vec,d,n,i,j):

    P = True

    for x in range(i,d + 1):
        for y in range(j,n):
            P = And( P, Not( T_gate_vec[x][y]) )

    return P

#Tゲートの後にHゲートが来るように調整
def restrict_gate_order(H_gate_vec, T_gate_vec, d, n, s):

    for i in range(d + 1):
        for j in range(n):
            #￢oterh_gate_vec[i][j]をすべてAndでつないだ論理式　i,j以降のT_gate_vecがFalseであるという論理式
            P = generate_restriction_of_other_gate_position(T_gate_vec,d,n,i,j)
            s.add(If(H_gate_vec[i][j],P,True))

def calc(input_list, output_set, n, num_of_var, node):

    d = 0;
    #ゲート数MAX_NUM_GATEまで探索
    while(d < MAX_NUM_GATE):
        gate = {}

        #d*n CNOTゲート群を表す変数
        c_vec = [[Bool("c_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d)]
        t_vec = [[Bool("t_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d)]
        #ゲートの配置を表す変数
        H_gate_vec = [[Bool("H_gate_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d + 1)]
        T_gate_vec = [[Bool("T_gate_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d + 1)]
        T_dagger_gate_vec = [[Bool("T_dagger_gate_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d + 1)]
        #論理状態を表す変数
        f_vec = [[BitVec("f_vec[%d,%d]" % (i,j), num_of_var) for j in range(n)] for i in range(d + 1)]
        for i in range(n):
            f_vec[0][i] =  BitVecVal(input_list[i], num_of_var)
        #z3-solver インスタンスの作成
        s = Solver()

        #このループ　関数内でええやん
        #ゲートごとに制約を追加
        for i in range(d):
            #同一ゲートはコントロールビットが一つしかない制約
            one_bit_per_gate(c_vec[i],n,s)
            one_bit_per_gate(t_vec[i],n,s)

        #出力を生成
        generate_output(f_vec, c_vec, t_vec, d, n, node)
        #出力と要求出力の一致

        equal_desired_output(f_vec, output_set, n, d, s, H_gate_vec, T_gate_vec, T_dagger_gate_vec)

        print("d=%d"%d)
        if(s.check() == sat):
            m = s.model()
            #display_gates(c_vec,t_vec,m,d,n)

            return convert_output(m,d,n,c_vec,t_vec)

        d += 1

def int_to_bit(num_list):
    res = 0;
    for i in num_list:
        res = res | (1 << i)

    return res

def adopt_gate(gate, bit_set):

    res = []

    for i, bit  in enumerate(bit_set):
        res.append([int_to_bit(bit), gate])

    return res

#回路を仮想化　　NNA制約を適応
def virtualy_calc(necessary_set, n, num_of_var, node, combi, gate):

    #ビット削減に伴い、変数を振り直して仮想的に小さい回路として扱う
    link = {} # bit -> virtual

    #仮想回路と実際に回路のリンクを作成
    for virtual_bit, bit in enumerate(combi['necessary_node']):
        link[bit] = virtual_bit

    #仮想回路の入力ビットを作成
    virtual_input = [(1 << n) for n in range(combi['num_node'])]

    #ノードを仮想化

    #使ってないノードを排除
    trimed_node = solve_combination.remove_unused_node(copy.copy(node), combi['necessary_node'])

    virtual_node = mapping.virtual_mapping(trimed_node, link)

    #necessary_setを仮想化
    virtual_necessary_set = []
    for set in necessary_set:
        virtual_set = []
        for logical_state in set:
            virtual_set.append(link[logical_state] )

        virtual_necessary_set.append(virtual_set)

    #necessary_setをビット化しなあかん
    virtual_necessary_set_bit = adopt_gate(gate, virtual_necessary_set)
    virtual_circuit = calc(virtual_input, virtual_necessary_set_bit, combi['num_node'], combi['num_node'], virtual_node)
    virtual_circuit = place_elementary_gate.place_gate(virtual_circuit, virtual_input, copy.copy(virtual_necessary_set_bit))

    circuit = [ [const.EMPTY for i in range(n) ]for j in range(len(virtual_circuit))]

    #仮想化して計算した回路を元に戻す
    for i in range(n):
        if(i in link.keys()):
            for j in range(len(virtual_circuit)):
                circuit[j][i] = virtual_circuit[j][link[i]]

    display.display_circuit(virtual_circuit)
    display.display_circuit(circuit)
    print(f'link:{link}')

    return circuit

# input = [1, 2, 4, 8, 16, 32]
# nce = [[29, 'T'], [32, 'T'], [17, 'T'], [19, 'T'], [51, 'T'], [50, 'T']]
# n = 6
# node = [[1, 2], [0, 3], [0, 4], [1, 5], [2, 5], [3, 4]]

# circuit = calc(input, nce, n, n, node)
# display.display_circuit(circuit)