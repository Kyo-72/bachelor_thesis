
#Tゲートが挿入される確率 = 1/T_GATE_PROBABILITY
#Tゲートが挿入される個数の期待値 NUM_T_GATE

#nビット、cnotゲート数dの回路を生成する
T_GATE_PROBABILITY = 5
NUM_T_GATE = 2

import random
import display
import desired_output

def generate_t_gate(n):
    res = [" " for i in range(n)]
    for i in range(n):
        #i番目のラインにtゲートを挿入するかの乱数(0なら生成)
        probability = random.randrange(NUM_T_GATE)
        if(not probability):
            res[i] = "T"

    
    

    return res
    
    

def generate_random_circuit(n,d):
    circuit = [["" for i in range(n)]]
    #depthをcnotゲートの数で初期化（Tゲートが加わる可能性）
    gate_depth = d
    for i in range(gate_depth):
        gate = [" " for j in range(n)]
        #remoteCNOTgateを生成する
        controll_bit = random.randrange(n)
        #controll_bitとtarget_bitで重複なし
        #NNAを満たさないCNOTのみ
        tmp = random.randrange(n)
        while( abs(controll_bit - tmp) < 2 ):
            tmp = random.randrange(n)
        target_bit = tmp


        gate[controll_bit] = "c"
        gate[target_bit] = "t"


        circuit.append(gate)

        
        
        #Tゲートを確率で生成する

        #tゲートを生成するかの乱数(0なら生成 or 最後は必ず)
        probability = random.randrange(T_GATE_PROBABILITY)
        if( not probability or i == gate_depth):
            gate = generate_t_gate(n)
            circuit.append(gate)
            #tゲートが追加されたので、depthが増加
            gate_depth += 1
            #イテレーターも増加

    return circuit
            

"""
n = 4
d = 15
random_circuit = generate_random_circuit(n,d)
random_circuit.pop(0)


display.display_circuit(random_circuit)
output_set = desired_output.desired_output([1,2,4,8],random_circuit)
print(output_set)
"""


