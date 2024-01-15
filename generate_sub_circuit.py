import const
import bit_search
import calc
import copy
import solve_combination
import const
import display
import const
import logic
import exception_handling.over_max_allowable_bit as except_over

#引数　　　　：　　　　部分回路ごとのnecessary_set input_list 量子ビット数 n 変数の数 num_of_var ノード　 node
#返り値　: 　　NNA-compliantな部分回路

def calc_bit_set(input_list, necessary_set):
    bit_set = {}

    #アウトプットを構成するため、必要な最小の量子ビットを計算する
    for i,output_state in enumerate(necessary_set):
        if(output_state[1] == const.HADAMARD_GATE or output_state[1] == const.OUTPUT):
            break
        bit_set[i] = bit_search.min_quantum_bit(input_list, abs(output_state[0]))

    return bit_set

#部分ごとに分ける
def sub_circuit(input_state, necessary_set, n, num_of_var, node):
    sub_circuit = []
    bit_set = calc_bit_set(input_state, necessary_set)

    #bit_setがなくなるまで探索
    while( len(necessary_set) != 0):
        #入力変数に応じて、bit_setを再計算する

        #bit_setから最適な組み合わせを見つける
        #TODO bit_setとnecessary_setを紐づける
        bit_combination = solve_combination.compute_handle_bits_combi(bit_set, node)
        un_nna_combination = {}

        for key,v in bit_combination.items():
            if(v['is_nna'] == False):
                un_nna_combination[key] = bit_combination[key]

        solve_combination.add_node_for_nna(node, un_nna_combination,8)

        adopted_combi = []
        max_score     = 0
        #ビットの組み合わせが要件を満たすかどうか
        adopted_combi = []
        max_score = 0
        for combi in bit_combination.values():
            #nnaがFalseかビットの数がmaxを超えてたらダメ
            if(combi['is_nna'] == False or len(combi['necessary_node']) > const.MAX_ALLOWABLE_NUM_OF_BIT):
                continue

            if(max_score < combi['num_combination']):
                max_score = combi['num_combination']
                adopted_combi = combi

        #TODO max_bitを超えてadopted_combiがない場合の処理を書く
        if(adopted_combi != []):
            #処理するbit_setを取り出す
            adopted_bit_set = []

            #選ばれたcombiを満たす回路を生成

            for i in adopted_combi['select_combi']:
                adopted_bit_set.append(bit_set[i])

            #処理したbit_setを削除する
            new_bit_set = {}
            new_necessary_set = []
            index = 0

            for i, state in bit_set.items():
                if(i not in adopted_combi['select_combi']):
                    #necessary_setを消す
                    new_necessary_set.append(necessary_set[i])
                    new_bit_set[index] = state
                    index += 1

            bit_set       = new_bit_set
            necessary_set = new_necessary_set

            #SMTソルバに入力，出力を投げてNNA回路を得る．
            sub_circuit += calc.virtualy_calc(copy.copy(adopted_bit_set), n, num_of_var, node, adopted_combi, const.T_GATE)
        # sub_circuit = place_elementary_gate.place_gate(sub_circuit, input_state, copy.copy(adopted_bit_set))
        else:
            #TODO ここに処理をかく
            #bit_setが1のやつを処理する #TODO 優先順位を考える(necessary_node少ないやつの方が良さそう)

            for combi in bit_combination.values():
                if(combi['num_combination'] == 1):
                    adopted_combi = combi
                    break

            logical_state = bit_set[ combi['select_combi'][0] ]
            subcircuit += except_over.handling_over_bit_circuit(node, adopted_combi, logical_state)

        display.display_circuit(sub_circuit)
        print('--------------------------')
        print(f"処理したnecessary_set :{necessary_set}")
        print(f'残りのnecessary_set :{new_bit_set}')

        #input_stateの更新
        output = logic.logical_state(input_state, sub_circuit)
        bit_set = calc_bit_set(output, necessary_set)

    return sub_circuit


# input_list = []
# necessary_set = []
# n = 4
# num_of_var = 4
# node = {}

# sub_circuit(input_list, necessary_set, n, num_of_var, node)
