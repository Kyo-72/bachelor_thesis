import logic
import copy
import display

elementary_gate_list = ["T","†","H","n","o"]

def retrieve_gate_index(gate,kinds_of_gate):

    return 0

def desired_output(init_state,circuit):
    d = len(circuit)
    n = len(circuit[0])
    output_set = []
    gate_type_list = []
    
    
    
    #elementary量子ゲートがあるなら要求出力を生成
    for i in range(d):
        
        gate = circuit[i]
        
        #elementary量子ビットの論理状態を要求出力集合へ
        
        gate_itr = []
        gate_type = " "
        #bitごとにelementaryゲートがないか探索
        for index,bit in enumerate(gate):
            #見つけたらgate_typeを更新
            if(len(gate_itr) == 0):
                for g in elementary_gate_list:
                    if(bit[0] == g):
                            gate_type = g
                            gate_itr.append(index)
                            break;
            #見つかった後はgate_typeは確定
            else:
                if(bit[0] == gate_type):
                    gate_itr.append(index)

        if(len(gate_itr) != 0):
              

            #ゲートまでの論理状態を取得
            x = logic.logical_state(init_state,circuit[0:i])
            
            
            #elementary量子ゲートがあるビットの論理状態を求め,要求出力集合へ
            set = []
            
            for t in gate_itr:
                set.append(x[t])


            
            output_set.append(copy.copy(list(set)))
            gate_type_list.append(gate_type)
            set.clear()
                

    
    
    
    return gate_type_list,output_set
                
                
            
            
        

    
