def pallelize_circuit(f):
    n = 0
    flag = 0
    previous_gate_type = " "
    previous_gate_bit = []

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
            gate = line.split(" ")
            gate_type = gate[0][0]
            gate_bit = []
            for bit in gate[1:n+1]:
                gate_bit.append(bit)
            #前のゲートと同じゲート
            if(gate_type == previous_gate_type):
                change_flag = 0
                for gate in gate_bit:
                    #一つ前のゲートと並列可能
                    if(gate not in previous_gate_bit):
                        previous_gate_bit.append(gate)
                        change_flag = 1
                #並列化処理が行われたら現在のgateは読み飛ばす
                if(change_flag == 1):continue
            
            previous_gate_bit = gate_bit
            previous_gate_type = gate_type
                        
                    

            

            

    