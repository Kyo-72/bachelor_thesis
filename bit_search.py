#ある論理状態を作るために必要な最小の量子ビットの集合をかえす
def min_quantum_bit(input_set, output_state):
    res_input_set = []
    n = len(input_set)
    for bit in range(1 << n):
        #使うインプットのindex
        ans_state = 0
        for i in range(n):
            if(bit & (1 << i)):
                ans_state = ans_state^input_set[i]
        
        if(ans_state == output_state):
            res_input_set = [i for i in range(n)  if bit & (1 << i)]
            break

    return res_input_set


