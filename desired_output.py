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
        
        #cnotじゃないビットの論理状態を要求出力集合へ
        if "c" not in gate:
            #elementary量子ゲートがあるビットを求める
            gate_itr = []
            #ゲートがある位置のindexを取る
            print(gate)
            for itr in range(n):
                #なにかゲートがあるならイテレータに追加
                if(gate[itr] != " " and gate[itr] != "g"):
                    gate_itr.append(itr)

            

            #Tゲートまでの論理状態を取得
            copy_circuit = copy.copy(circuit)
            x = logic.logical_state(init_state,circuit[0:i])
            
            
            #tゲートがあるビットの論理状態を求め,要求出力集合へ
            set = []
            
            for t in gate_itr:
                set.append(x[t])

            
            output_set.append(copy.copy(list(set)))
            set.clear()
            

    
    
    
    return output_set
                
                
            
            
        

    
