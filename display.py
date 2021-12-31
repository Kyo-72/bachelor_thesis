import const

#circuitと出力xを渡すと、回路を表示するプログラム
def display_circuit(circuit,x=None):
    d = len(circuit)
    if(d == 0):
        return 0
    n = len(circuit[0])
    
    
    for j in range(n):
    
        for i in range(d):
        
            print("ー",end="")
            gate = circuit[i][j]
            
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

        
        
        if(x != None):
            print(":%d"%(x[j]),end="")

        print()
        
