import const
import logic
import display

#要求出力の中で第一引数の論理関数と一致する関数を返す　
def macth_gate(logical_state,output_set):
    res = []
    #回路における論理関数と要求関数が等しいゲートを探す
    for gate in output_set:
        if gate[0] == logical_state:
            res.append(gate)
    #回路における論理関数と要求関数が等しいゲートを消す
    output_set = [gate for gate in output_set if gate[0] != logical_state]

    return res

def generate_elementary_gate_bolck(gate_list,index):
    gate = []
    for i,g in enumerate( gate_list ):
        if(i == index):
            gate.append(g[1])
        else:
            gate.append(" ")

    return gate

def split_gate(output_set,H_gate_list,other_gate_list):

    for out in output_set:
        #アダマールかアウトプット
        if out[1] == const.HADAMARD_GATE or out[1] == const.OUTPUT:
            H_gate_list.append(out)

        #TゲートかTダガーゲート
        elif out[1] == const.T_GATE or out[1] == const.T_DAGGER_GATE:
            other_gate_list.append(out)


def place_T_gate(T_gate_list,circuit,inserted_circuit,init_state):

    gate = []

    #CNOTゲートからなる回路のすべての論理関数を探索
    for depth in range( 1 , len(circuit) ) :
        #CNOTゲートをくっつける
        inserted_circuit.append(circuit[depth - 1])
        #論理関数を計算(そのブロックまでの)
        x = logic.logical_state(init_state,circuit[:depth])
        #探索対象の論理関数に作用させるべきTゲートがあるかどうか（複数可）
        for index,logical_state in enumerate(x):
            match_gate_list = macth_gate(logical_state,T_gate_list)
            gate = generate_elementary_gate_bolck(match_gate_list,index)

        #作用させるべきTゲートがあれば回路に挿入する
        for g in gate:
            inserted_circuit.append(g)

def place_H_gate(H_gate_list,circuit,inserted_circuit,init_state):
    gate = []

    #CNOT回路の末端上の論理関数を計算
    x = logic.logical_state(init_state,circuit)
    #ゲートがない論理状態を消す（論理関数が負の数）
    H_gate_list = [gate for gate in H_gate_list if gate[1] >= 0]

    for index,logical_state in enumerate( circuit[len(circuit) - 1] ):
        match_gate_list = macth_gate(logical_state,H_gate_list)
        gate = generate_elementary_gate_bolck(match_gate_list,index)

    #TODO 並列化を行う
    #作用させるべきTゲートがあれば回路に挿入する
    for g in gate:
        inserted_circuit.append(g)

def place_gate(init_state,circuit,output_set):

    inserted_circuit = []
    #HゲートとTゲートで動作が変わるため分けて扱う
    H_gate_list = []
    T_gate_list = []

    print(circuit)

    split_gate(output_set,H_gate_list,H_gate_list)

    #Tゲートから配置する
    place_T_gate(T_gate_list,circuit,inserted_circuit,init_state)
    place_H_gate(H_gate_list,circuit,inserted_circuit,init_state)

    print(inserted_circuit)
    display.display_circuit(inserted_circuit)


    #Tゲートの後にHゲートを配置する

    # for depth in range( 1 , len(circuit) ) :
    #     #論理関数を計算(そのブロックまでの)
    #     inserted_circuit.append(circuit[depth - 1])
    #     x = logic.logical_state(init_state,circuit[:depth])
    #     for index,logical_state in enumerate(x):
    #         match_gate_list = macth_gate(logical_state,output_set)
    #         gate = generate_elementary_gate_bolck(match_gate_list,index)

    #     for g in gate:
    #         inserted_circuit.append(g)

    # inserted_circuit.append(circuit[-1]

# circuit = [['t', 'c', ' ', ' '], [' ', ' ', 'c', 't'], ['c', 't', ' ', ' '], [' ', 'c', 't', ' '], ['t', 'c', ' ', ' '], [' ', 't', 'c', ' '], [' ', ' ', 't', 'c'], [' ', 'c', 't', ' '],[' ', ' ', 't', 'c'], [' ', ' ', 'c', 't'], 
# [' ', ' ', 't', 'c'], [' ', 'c', 't', ' '], ['c', 't', ' ', ' '], ['t', 'c', ' ', ' '], [' ', 't', 'c', ' '], ['c', 't', ' ', ' '],[' ', 'c', 't', ' '], ['c', 't', ' ', ' '], [' ', 'c', 't', ' ']]

# output_set = [[(-1, 'H'), (-2, 'H'), (-4, 'H'), (8, 'H')], [(1, 'T'), (4, 'T'), (16, 'T'), (17, 'R'), (5, 'R'), (4, 'R'), (16, 'T'), (-21, 'H'), (-2, 'H'), (-4, 'H'), (20, 'H')], [(-21, 'H'), (-2, 'H'), (-4, 'H'), (32, 'H')], [(21, 'T'), (2, 'T'), (64, 'T'), (85, 'R'), (23, 'R'), (2, 'R'), (64, 'T'), (-87, 'H'), (-2, 'H'), (-4, 'H'), (66, 'H')], [(2, 'o'), (6, 'o'), (83, 'o'), (128, 'o')]]
# init_state = [1,2,4,8]
# place_gate(init_state,circuit,output_set)



