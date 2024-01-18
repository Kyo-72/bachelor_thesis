import logic
import display
import time
import copy
import desired_output
import read_file
import os
import aggregate
import mapping
import generate_sub_circuit
import sys
import const

print(os.getcwd())

def inti_output(n):
    print(os.getcwd())
    os.chdir("../../output")
    with open("my_{}bit_output.txt".format(n),"w") as output:
        output.write("ファイル名 | 分解前ゲート数 | 分解後ゲート数 | 実行時間\n")

    os.chdir("../")

def init_config(n):

    init_state = []
    inti_output(n)
    for i in range(n):
        x = (1<<i)
        init_state.append(x)

    return init_state

def end_config(num_of_circuit,file_name,sum,n):
    os.chdir("./output")
    with open("my_{}.txt".format(file_name),"a") as output:
        output.write("\n\n平均実行時間{}s\n".format(sum/num_of_circuit))

    os.chdir("../")


#テスト回路のリストを取得する
print("実験用回路のディレクトリ名を入力してください")
# dir_name = input()
dir_name = "tekitou"
test_list = os.listdir(path="./input/{}".format(dir_name))
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
    print(circuit)
    #回路からビット数を読み込む
    n = len(circuit[0])

    node = mapping.bit_mapping(n)

    #初期状態を設定
    init_state = init_config(n)
    #要求出力集合
    output_set = [init_state]

    #回路からゲートの種類と要求出力集合を得る
    subircuits_output_info = desired_output.divide_circuit(init_state,circuit)
    input_list = subircuits_output_info[0]
    output_set = subircuits_output_info[1]
    num_of_var = subircuits_output_info[2]
    #回路の最終的な論理状態を取得
    x = logic.logical_state(init_state,circuit)
    #分解前の回路を出力Z
    display.display_circuit(circuit,x)
    #要求出力集合を出力
    # print(output_set)

    divied_num = len(output_set)

    #分解前回路ゲート数
    print("CNOTゲート数{}".format( aggregate.count_cnot(circuit) ) )

    #開始時間
    start = time.time()

    #分解後の回路
    decomposed_circuit = []
    #要求集合に基づいて回路を分解する
    for block in range( len(output_set) ):
        #各部分回路の 
        print(output_set)

        #部分的な回路を生成し,decoposed_circuitにつなげる
        print("今回の回路の入力{}".format( input_list[block] ) )
        print("今回の回路の出力{}".format( output_set[block] ) )

        sub_circuit = generate_sub_circuit.sub_circuit(input_list[block], output_set[block], n, num_of_var, node)

        for gate in sub_circuit:
            decomposed_circuit.append(copy.copy(gate))

        if(len(circuit) != 0):
            x = logic.logical_state(input_list[block],circuit)
        else:
        #部分回路内のCNOTゲートが0だったら出力はinputと同じ
            x = input_list[block]

        print("実際の出力{}".format(x))

        gate = []
        display.display_circuit(circuit,x,input_list[block])
        if(block < len(output_set) - 1):
            for qubit, gate_type in enumerate(circuit[-1]):
                if(gate_type == const.HADAMARD_GATE or qubit == const.OUTPUT):
                    continue
                input_list[block + 1][qubit] = copy.copy(x[qubit])
        decomposed_circuit.append(copy.copy(gate))

    decomposed_circuit.pop(0)
    #出力の論理状態を取得
    x = logic.logical_state(init_state,decomposed_circuit)
    #回路を出力する
    display.display_circuit(decomposed_circuit,x)
    print(decomposed_circuit)
    #実行時間を計測
    process_time = time.time() - start
    num_of_circuit += 1
    aggregate.aggregate_result(file_name,source_circuit,decomposed_circuit,process_time)
    sum += process_time

    print("所要時間:{}s".format(process_time))
    print("分割数:{}".format(divied_num))

end_config(num_of_circuit,file_name,sum,n)



