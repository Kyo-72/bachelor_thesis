NUM_OF_SPACE = 10

import const

#circuitと出力outputを渡すと、回路を表示するプログラム
def display_circuit(circuit,output=None,input=None):
    d = len(circuit)
    if(d == 0):
        return 0
    n = len(circuit[0])

    for j in range(n):

        if(input != None):
            print("%d"%(input[j]),end="")
            keta = len( str(input[j]) )
            for k in range(NUM_OF_SPACE - keta):
                print(" ",end="")

            print(":",end="")

        for i in range(d):

            #空文字列の時の処理
            try:
                print("ー",end="")
                gate = circuit[i][j]
            except IndexError:
                continue

            if(gate == const.CONTROLL_BIT):
                print("・",end="")
            elif(gate == const.TARGET_BIT):
                print("〇",end="")
            elif(gate == const.T_GATE):
                print("Ｔ",end="")
            elif(gate == const.HADAMARD_GATE):
                print("Ｈ",end="")
            elif(gate == const.T_DAGGER_GATE):
                print("ｔ",end="")
            else:
                print("ー",end="")

        if(output != None):
            print(":%d"%(output[j]),end="")

        print()

    print()

