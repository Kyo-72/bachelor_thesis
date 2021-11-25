import logic
import copy
import display

def desired_output(init_state,circuit):
    d = len(circuit)
    n = len(circuit[0])
    output_set = []
    
    
    
    #tゲートがあるなら要求出力を生成
    for i in range(d):
        
        gate = circuit[i]
        
        #最後のtゲートがあるdepth
        
        #tゲートがあるビットの論理状態を要求出力集合へ
        if "T" in gate:
            #tゲートがあるビットを求める
            idx = -1
            t_gate_bit = []
            for count in range(gate.count("T")):
                idx = gate.index("T",idx + 1)
                t_gate_bit.append(idx)

            

            #Tゲートまでの論理状態を取得
            copy_circuit = copy.copy(circuit)
            x = logic.logical_state(init_state,circuit[0:i])
            
            
            
            set = []
            
            
            for bit in range(n):
                #tゲートの有無関係なくの論理状態を求め,要求出力集合へ
                set.append(x[bit])
                

            
            output_set.append(copy.copy(list(set)))
            set.clear()
            

    
    
    
    return output_set
                
                
            
            
        

    
