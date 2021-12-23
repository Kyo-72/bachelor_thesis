import display

def convert_toffoli_into_cnot(line):
    #分解後のゲート群を入れる変数
    gates = ""
    controll_bit= []
    bit = line.split(" ")
    #controll_bit一つ目
    controll_bit.append(bit[1])
    #controll_bit二つ目
    controll_bit.append(bit[2])
    #ターゲットビット
    target_bit = bit[3][0]

    #Clifford+Tゲート群に分解
    gates += "H1 {}\n".format(target_bit)
    gates += "T3 {} {} {}\n".format(controll_bit[0],controll_bit[1],target_bit)
    gates += "t2 {} {}\n".format(controll_bit[1],controll_bit[0])
    gates += "t2 {} {}\n".format(target_bit,controll_bit[1])
    gates += "t2 {} {}\n".format(controll_bit[0],target_bit)
    gates += "†1 {}\n".format(controll_bit[1])
    gates += "t2 {} {}\n".format(controll_bit[0],controll_bit[1])
    gates += "†2 {} {}\n".format(controll_bit[0],controll_bit[1])
    gates += "T1 {}\n".format(target_bit)
    gates += "t2 {} {}\n".format(target_bit,controll_bit[1])
    gates += "t2 {} {}\n".format(controll_bit[0],target_bit)
    gates += "t2 {} {}\n".format(controll_bit[0],controll_bit[1])
    gates += "H1 {}\n".format(target_bit)

    return gates

def convert_mct_into_toffoli(line,num_of_io):
    return line

def decompose(file_name):
    #分解後回路.最後にファイルに書き込む
    new_circuit = ""
    flag = 0

    with open(str) as f:
        
        
        for line in f:
 
            if(".numvars" in line):
               n = int( line.split(" ")[1] )
        
            #beginからゲートを読み始める(flag = 1)
            if(".begin" in line):
                flag = 1
            #endが来たら読み込み終了
            elif(".end" in line):
                break
            #flag = 1 ならゲートを読み込む
            elif(flag):
                #ファイルを区切りリスト
                gate = line.split(" ")
                #ゲートの種類
                type_of_gate = gate[0][0]
                #ゲートの入出力の数
                num_of_io = int( gate[0][1] )
                #MCT,NTCを分解する
                if(type_of_gate == "t"):
                    
                    #Toffoliゲート分解.
                    if(num_of_io == 3):
                        new_circuit += convert_toffoli_into_cnot(line)
                    #MTCゲートをtoffoliに分解後,clifford+tゲート群に分解
                    elif(num_of_io > 3):
                        line = convert_mct_into_toffoli(line,num_of_io)
                        line = convert_toffoli_into_cnot(line)
                    else:
                        new_circuit += line

                    #分解後は元のゲートは追加しなくていい
                    continue

            #分解しない行はそのまま追加
            print(line)
            new_circuit += line 
                    


            

                
                
              
                
    with open(str,mode="w") as f:
        f.write(new_circuit)

    return 0

str = "input/revlib/ham7.txt"
#str += input()
decompose(str)
