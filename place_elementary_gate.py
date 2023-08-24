import const
import logic
import copy
import display

T_gate_set = []
T_dagger_gate_set = []
H_gate_set = []
insert_last_gate = []

d = 0
n = 0

 #単一ゲート挿入用辞書　キーは挿入列index, 値は挿入するカラムのリスト
insert_gate = {}

def isnert_t_gate(state, i, j):
    gate_sets = {const.T_GATE:T_gate_set, const.T_DAGGER_GATE:T_dagger_gate_set}

    for gate_type, gate_states in gate_sets.items():
        for gate_state in gate_states[:]:
            if(abs(gate_state) == state):
                insert_gate[i].append( [(gate_type)if row == j else (const.EMPTY)for row in range(n)] )
                #配置したゲートは削除
                gate_states.remove(gate_state)
    
def append_last_gate(circuit, init_state):
    global insert_last_gate
    last_states = logic.logical_state(init_state,circuit) 
    insert_last_gate = ( [(const.HADAMARD_GATE)if state in H_gate_set else (const.EMPTY) for state in last_states] )

def place_gate(circuit,init_state, output):

    global insert_gate, insert_last_gate, d

    d = len(circuit)
    insert_gate = {i:[] for i in range(d + 1)}
    last_gate = []
    
    #各ゲートの要求出力をリストに変換
    for o in output:
        gate = o[1]
        v = o[0]
        if(gate == const.HADAMARD_GATE):
            H_gate_set.append( v )
        elif(gate == const.T_GATE):
            T_gate_set.append( v )
        elif(gate == const.T_DAGGER_GATE):
            T_dagger_gate_set.append( v )

    for i in range(d):
        states = logic.logical_state(init_state,circuit[:i]) 
        for j, state in enumerate(states):
            #(i , j)番目の論理状態に一致するT/T_daggerゲートを探索、insert_gateの該当番地に単一ゲートを追加
            isnert_t_gate(state ,i, j)
    
    #Hゲートとoutputをゲートのお尻につける
    append_last_gate(circuit,init_state)
            

    res_circuit = []
    for i,c in enumerate(circuit):
        res_circuit.append(c)
        if(len(insert_gate[i]) != 0):
            for insert_gate_col in insert_gate[i]:
                res_circuit.append(insert_gate_col)
    #最後のHゲートを付ける
    res_circuit.append(insert_last_gate)


    print('res')
    display.display_circuit(res_circuit)
    return res_circuit




    