import calc
import logic
import display
import time
import copy
import desired_output
import read_file
import read_file
import os



while(1):
    
    print("入力ビットの数を入力してください(0でプログラム終了):")
    n = int(input())

    if(n == 0):
        break

    init_state = []
    for i in range(n):
        x = (1<<i)
        init_state.append(x)
    
    #要求出力集合
    desired_output_set = [init_state]
    os.chdir('/Users/DELL/ソースコード')
    
    #ファイルから回路を入力する
    circuit = read_file.read_file("input/{}bit_circuit/circuit1.txt".format(n))
    
    #回路から要求出力集合を得る
    desired_output_set = desired_output.desired_output(init_state,circuit)

    #分解前の回路を出力
    x = logic.logical_state(init_state,circuit)
    display.display_circuit(circuit,x)
    #要求出力集合を出力
    print(desired_output_set)


    #開始時間
    start = time.time()
    
    #分解後の回路
    decomposed_circuit = [[]]
    #input_listの初期化
    input_list = init_state
    depth = 0
    #要求集合に基づいて回路を分解する
    for block in range( len(desired_output_set )):
        
        #部分的な回路を生成し,decoposed_circuitにつなげる
        output_list = desired_output_set[block]
        circuit = calc.calc(input_list,output_list,n)
        display.display_circuit(circuit)
        for gate in circuit:
            decomposed_circuit.append(copy.copy(gate))
        
        #要求出力が生成されているビットにTゲートをつなげる
        x = logic.logical_state(input_list,circuit)
        gate = []
        #最後はTゲートはつなげなくていい
        
            
        for bit in x:
            if(bit in output_list):
                gate.append("T")
            else:
                gate.append(" ")

        decomposed_circuit.append(copy.copy(gate))
        #出力を次の入力に更新
        input_list = x

    
    decomposed_circuit.pop(0)
    #出力の論理状態を取得
    x = logic.logical_state(init_state,decomposed_circuit)
    #回路を出力する
    display.display_circuit(decomposed_circuit,x)
    process_time = time.time() - start
   
    
    
    
    print("所要時間:%ds"%process_time)
    
    

#目的出力関数を得る

#ゲートを分解し、回路を更新




