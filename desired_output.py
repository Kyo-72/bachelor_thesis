import logic
import copy
import display
import const

elementary_gate_list = [const.T_GATE,const.T_DAGGER_GATE,const.HADAMARD_GATE,const.OUTPUT]

def retrieve_gate_index(gate,kinds_of_gate):

    return 0

def desired_output(init_state,circuit):
    d = len(circuit)
    n = len(circuit[0])
    input_list = []
    input_list.append( copy.copy(init_state) )
    output_set = []
    gate_type_list = []
    pre_gate_depth = 0
    #変数の数　量子ビットの数で初期化．Hゲートが出てくると増やす
    num_of_var = n
    
    
    
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
            #部分回路だけに変更
            sub_circuit = circuit[pre_gate_depth:i]
            
            if( len(sub_circuit) != 0):
                x = logic.logical_state(init_state,sub_circuit)
            else:
            #部分回路内にCNOTゲートがなければ
                x = copy.copy( input_list[-1] )

            #今回の部分回路の末尾が何ゲート目かを保存
            pre_gate_depth = i + 1
            
            
            #elementary量子ゲートがあるビットの論理状態を求め,要求出力集合へ
            set = []
            
           #Tゲートなら要求出力は集合
            if(gate_type != const.HADAMARD_GATE):
                for t in gate_itr:
                    set.append(x[t])
            else:
            #Hゲートなら要求出力は順列(全て要求を満たす必要がある)
                for i in range(len(x)):
                    if(i in gate_itr):
                        set.append(x[i])
                    else:
                        set.append(-x[i])

            #ゲートタイプがHなら，入力に新たな変数を追加
            if(gate_type == const.HADAMARD_GATE):
                for t in gate_itr:
                    #最新の変数（ビットベクトルの最上位ビット）を追加
                    new_var = (1 << num_of_var) 
                    #更新した変数で，xを更新
                    x[t] = new_var
                    #変数の数を更新
                    num_of_var += 1
            #入力リストを更新
            input_list.append(x)


            #次の入力を，今回の部分回路における出力で更新
            init_state = x
            output_set.append(copy.copy(list(set)))
            gate_type_list.append(gate_type)
            set.clear()
                


    print("---------------input------------------")
    print(input_list)
    print("---------------output------------------")
    print(output_set)
    return gate_type_list,input_list,output_set,num_of_var
                
                
            
            
        

    
