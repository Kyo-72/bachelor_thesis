import os
import const
#read_file revliv形式の量子ゲート群をリストに変換.ファイル名を指定すると二次元リストで返す




#" "⇒何もなし
#"c"⇒コントロールビット
#"t"⇒ターゲットビット
#"T"⇒Tゲート
#"R"⇒Tダガーゲート
#"H"⇒Hゲート
#"n"⇒NOTゲート
#"G"⇒ガーベッジビット
#"f"⇒要求出力ビット
#"out_*"⇒出力ビット



elementary_gate_list = [const.T_GATE,const.T_DAGGER_GATE,const.HADAMARD_GATE,const.OUTPUT]


#例[[" ","c","t"],[" ","T"," "]]

def add_elementary_gate(type_of_gate,gate,n,input):
    gate_list = [" " for i in range(n)]
    for bit in gate:
        gate_list[input.index(bit)] = type_of_gate

    return gate_list

def convert_to_list(n,line,input):
    gate_list = [" " for i in range(n)]
    
    #ファイルを区切りリスト
    gate = line.split(" ")
    #ゲートの種類
    type_of_gate = gate[0][0]
    #ゲートの入出力の数
    num_of_io = int( gate[0][1] )
    #末尾の改行文字を処理
    try:
        gate[num_of_io] = gate[num_of_io].split("\n")[0]
    except IndexError:
        print("index error occured")
        print(line)

    #bit毎に文字列に変換する

    #1量子bitゲート

    for g in elementary_gate_list:
        if(type_of_gate == g):
            gate_list = add_elementary_gate(g,gate[1:num_of_io + 1],n,input)
  
        
    if(type_of_gate == const.TARGET_BIT):
        
    #MCTゲート

        #notゲート
        if(num_of_io == 1):
            n_bit = gate[num_of_io][0]
            gate_list[ input.index(n_bit) ] = "n"
        else:
        
            #コントロールビットについてbit毎に文字列に変換
            for i in range(1,num_of_io):
                controll_bit = gate[i]
                gate_list[ input.index(controll_bit)] = const.CONTROLL_BIT

            #最後の一ビットはターゲットビット
            target_bit = gate[num_of_io].split("\n")[0]
            gate_list[ input.index(target_bit)] = const.TARGET_BIT

    return gate_list
    

def read_file(str):
    #lineの数
    d = 0
    flag = 0
    #リスト形式でゲートを表現
    circuit = []
    input=[]
    kinds_of_output = []
    

    #TODO MCTゲート 分解
    #TODO Toffoli分解
    
    #TODO 優先順位 並行処理出来るゲートを並列化
    

    
    #ファイルから一行ずつ読み込む
    with open(str) as f:
        
        
        for line in f:

            
            
            if(".numvars" in line):
               n = int( line.split(" ")[1] )
            #outputを読み込む

            if(".variables" in line):
                #量子ビットの上位からinputに入れる
                input = line.split(" ")[1:n + 1]
                #改行文字処理
                input[n - 1] = input[n - 1].split("\n")[0]

            if(".output" in line):
                kinds_of_output = line.split(" ")[1:n + 1]
                #改行文字を消去
                kinds_of_output[n - 1] = kinds_of_output[n - 1].split("\n")[0]

                #output_bitをより分かりやすく(c ⇒　out_c)
                for i in range( len(kinds_of_output) ):
                    kinds_of_output[i] = "out_" + kinds_of_output[i]

            #garbageビットを読み取る
            if(".garbage" in line):
                garbage = line.split(" ")[1]
                #末尾のnull文字消去
                garbage = garbage.split("\n")[0]
                
                for i,g in enumerate(garbage):
                    if(g == "1"):
                        kinds_of_output[i] = const.GARBAGE_BIT
        
            #beginからゲートを読み始める(flag = 1)
            if(".begin" in line):
                flag = 1
            #endが来たら読み込み終了
            elif(".end" in line):
                break
            #flag = 1 ならゲートを読み込む
            elif(flag):

                gate_list = []
                #ゲートをリストにする
                gate_list = convert_to_list(n,line,input)
                circuit.append(gate_list)
                #ToDoゲートの最後の要求出力をリストの末尾にappendする
              
    circuit.append(kinds_of_output) 
    return circuit



                

