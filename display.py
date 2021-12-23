
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
            
            if(gate == "c"):
                print("・",end="")
            elif(gate == "t"):
                print("〇",end="")
            elif(gate == "T"):
                print("Ｔ",end="")
            elif(gate == "H"):
                print("Ｈ",end="")
            elif(gate == "†"):
                print("†",end="")
            else:
                print("ー",end="")

        
        
        if(x != None):
            print(":%d"%(x[j]),end="")

        print()
        
