import logic
import copy
import display

elementary_gate_list = ["T","†","H","n"]

def retrieve_gate_index(gate,kinds_of_gate):

    return 0

def desired_output(init_state,circuit):
    d = len(circuit)
    n = len(circuit[0])
    output_set = []
    gate_type = []
    
    
    
    #elementary量子ゲートがあるなら要求出力を生成
    for i in range(d):
        
        gate = circuit[i]
        
        #elementary量子ビットの論理状態を要求出力集合へ

        for g in elementary_gate_list:


            if g in gate:
                gate_type.append(g)
                #elementary量子ゲートがあるビットを求める
                gate_itr = []
                #ゲートがある位置のindexを取る
                print(gate)
                for itr in range(n):
                    #ゲートがあるならイテレータに追加
                    if(gate[itr] != " " and gate[itr] != "g"):
                        gate_itr.append(itr)

                

                #ゲートまでの論理状態を取得
                copy_circuit = copy.copy(circuit)
                x = logic.logical_state(init_state,circuit[0:i])
                
                
                #elementary量子ゲートがあるビットの論理状態を求め,要求出力集合へ
                set = []
                
                for t in gate_itr:
                    set.append(x[t])


                
                output_set.append(copy.copy(list(set)))
                set.clear()
            

    
    
    
    return gate_type,output_set
                
                
            
            
        

    
