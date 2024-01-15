#inputと回路から出力の論理状態を整数型リストで返す
import copy
import const

def logical_state(init_state,circuit):
    #ゲートがないならinput_listを返す
    if(len(circuit) == 0):
        return init_state

    d = len(circuit)
    n = len(circuit[0])
    x = copy.copy(init_state)


    for i in range(d):
        c_bit = -1;
        #iゲート目のコントロールビットを見つける
        if "c" not in circuit[i]:
            continue

        for j in range(n):
            if(circuit[i][j] == const.CONTROLL_BIT):
                c_bit = j
        #iゲート目のターゲットビットにコントロールビットの論理状態をxorする
        for j in range(n):
            if(circuit[i][j] == const.TARGET_BIT):
                x[j] = x[c_bit] ^ x[j]

    return x

