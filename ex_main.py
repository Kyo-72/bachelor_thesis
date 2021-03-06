import ex_calc as calc
import logic
import display
import time
import copy
import ex_desired_output as desired_output
import read_file
import os
import aggregate
import const



def inti_output(n):
    os.chdir("../../output")
    with open("my_{}bit_output.txt".format(n),"w") as output:
        output.write("ファイル名　| 分解前ゲート数 | 分解後ゲート数 | 実行時間\n")
        
    os.chdir("../")

def init_config(n):


    init_state = []
    inti_output(n)
    for i in range(n):
        x = (1<<i)
        init_state.append(x)

    return init_state

def end_config(num_of_circuit,sum,n):
    os.chdir("./output")
    with open("my_{}bit_output.txt".format(n),"a") as output:
        output.write("\n\n平均実行時間{}s\n".format(sum/num_of_circuit))
        
    os.chdir("../")



#テスト回路のリストを取得する
print("実験用回路のディレクトリ名を入力してください")
dir_name = input()
test_list = os.listdir(path="input/{}".format(dir_name))
#実行時間の合計
sum = 0
#実行した回路の数
num_of_circuit = 0;

#ディレクトリ内の回路全て分解する
for file_name in test_list:


    #テスト用回路のディレクトリ移動する
    os.chdir('./input/{}'.format(dir_name))
    
    #ファイルから回路を読み込む
    source_circuit = read_file.read_file(file_name)
    circuit = copy.copy(source_circuit)

    #回路からビット数を読み込む
    n = len(circuit[0])
    print(n)

    #初期状態を設定
    init_state = init_config(n)
    #要求出力集合
    output_set = [init_state]

    #回路からゲートの種類と要求出力集合を得る
    subircuits_output_info = desired_output.desired_output(init_state,circuit)
    gate_type = subircuits_output_info[0]
    output_set = subircuits_output_info[1]
    num_of_var = subircuits_output_info[2]
    #回路の最終的な論理状態を取得
    x = logic.logical_state(copy.copy(init_state),circuit)
    #分解前の回路を出力
    display.display_circuit(circuit,x)
    #要求出力集合を出力
    print(output_set)
    


    #開始時間
    start = time.time()

    #分解後の回路
    decomposed_circuit = [[]]
    #要求集合に基づいて回路を分解する
    for block in range( len(output_set) ):
    
        #部分的な回路を生成し,decoposed_circuitにつなげる
        print("今回の回路の入力{}".format( init_state ) )
        print("今回の回路の出力{}".format( output_set[block] ) )
        circuit = calc.calc(copy.copy(init_state),copy.copy(output_set[block]),n,num_of_var,gate_type[block])

        for gate in circuit:
            decomposed_circuit.append(copy.copy(gate))
        
        if(len(circuit) != 0):
            x = logic.logical_state(copy.copy(init_state),circuit)
        else:
        #部分回路内のCNOTゲートが0だったら出力はinputと同じ
            x = copy.copy(init_state)

        print("実際の出力{}".format(x))

        gate = []
        display.display_circuit(circuit,x,copy.copy(init_state))
        
        #単一量子ゲートをつなげる
        for i,bit in enumerate(x):
            if(bit in output_set[block]):
                if(output_set[block][i] < 0):
                    gate.append(" ")
                else:
                    gate.append(gate_type[block])
            else:
                gate.append(" ")

    
        decomposed_circuit.append(copy.copy(gate))

        #Hゲートがない場合，出力を次の入力に更新
        # if(gate_type[block] != const.HADAMARD_GATE):
        #     input_list[block + 1] = x
        # else:
        #     print(x)
        #     for i,bit in enumerate(x):
        #         #Hゲートがある場合，更新しなくていい
        #         if(bit not in output_set[block]):
        #             #Hゲートがないbitは前回の回路の出力で更新
        #             input_list[block + 1][i] = bit
                




    decomposed_circuit.pop(0)
    #出力の論理状態を取得
    x = logic.logical_state(init_state,decomposed_circuit)
    #回路を出力する
    display.display_circuit(decomposed_circuit,x)
    print(decomposed_circuit)
    #実行時間を計測
    process_time = time.time() - start
    num_of_circuit += 1
    aggregate.aggregate_result(file_name,source_circuit,decomposed_circuit,n)
    sum += process_time




    print("所要時間:%fs"%process_time)
    
    
end_config(num_of_circuit,sum,n)



