import const
import bit_search
import calc
import copy


#引数　　　　：　　　　部分回路ごとのnecessary_set input_list 量子ビット数 n 変数の数 num_of_var ノード　 node
#返り値　: 　　NNA-compliantな部分回路

#部分ごとに分ける
def sub_circuit(input_list, necessary_set, n, num_of_var, node):
    sub_circuit = []
    bit_set     = {}

    #アウトプットを構成するため、必要な最小の量子ビットを計算する
    for i,output_state in enumerate(necessary_set):
        if(output_state[1] == const.HADAMARD_GATE or output_state[1] == const.OUTPUT):
            break
        bit_set[i] = bit_search.min_quantum_bit(input_list, abs(output_state[0]))

    #SMTソルバに入力，出力を投げてNNA回路を得る．
    sub_circuit = calc.calc(input_list, copy.copy(necessary_set), n, num_of_var, node)
    sub_circuit = place_elementary_gate.place_gate(circuit, input_list, copy.copy(output_set))

    return sub_circuit
