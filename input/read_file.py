import os
#read_file revliv形式の量子ゲート群をリストに変換.ファイル名を指定すると二次元リストで返す


#" "⇒何もなし
#"c"⇒コントロールビット
#"t"⇒ターゲットビット
#"T"⇒Tゲート
#"n"⇒NOTゲート


#例[[" ","c","t"],[" ","T"," "]]
os.chdir('/Users/DELL/ソースコード/input')



def convert_to_list(d,line):
    gate_list = [" " for i in range(d)]
    
    #ファイルを区切りリストへ
    gate = line.split(" ")
    #ゲートの種類
    type_of_gate = gate[0][0]
    #ゲートの入出力の数
    num_of_io = int( gate[0][1] )
    #bit毎に文字列に変換する

    #Tゲート
    if(type_of_gate == "T"):
        for i in range(1,num_of_io):
            T_gate_bit = gate[i]
            gate_list[ord(T_gate_bit) - ord("a")] = "T"
            
        T_gate_bit = gate[num_of_io][0]
        gate_list[ord(T_gate_bit) - ord("a")] = "T"    
        
    elif(type_of_gate == "t"):
        
    #MCTゲート

        #notゲート
        if(num_of_io == 1):
            n_bit = gate[num_of_io][0]
            gate_list[ ord(n_bit) - ord("a")] = "n"
        else:
        
            #コントロールビットについてbit毎に文字列に変換
            for i in range(1,num_of_io):
                controll_bit = gate[i]
                gate_list[ ord(controll_bit) - ord("a")] = "c"

            #最後の一ビットはターゲットビット
            target_bit = gate[num_of_io][0]
            gate_list[ ord(target_bit) - ord("a")] = "t"

    return gate_list
    

def read_file(str):
    #lineの数
    d = 0
    flag = 0
    #リスト形式でゲートを表現
    circuit = []
    

    
    #ファイルから一行ずつ読み込む
    with open(str) as f:
        for line in f:

            
            
            if(".numvars" in line):
               d = int( line.split(" ")[1] ) 
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
                gate_list = convert_to_list(d,line)
                circuit.append(gate_list)

    return circuit




                

