import calc
import logic
import display
import time
import copy
import desired_output
import read_file
import os
import aggregate

def inti_output(n):
    os.chdir("/Users/DELL/ソースコード/output")
    with open("my_{}bit_output.txt".format(n),"w") as output:
        output.write("ファイル名　| 分解前ゲート数 | 分解後ゲート数 | 実行時間\n")
        
    os.chdir("/Users/DELL/ソースコード")

def init_config(n):


    init_state = []
    inti_output(n)
    for i in range(n):
        x = (1<<i)
        init_state.append(x)

    return init_state

def end_config(num_of_circuit,sum,n):
    os.chdir("/Users/DELL/ソースコード/output")
    with open("my_{}bit_output.txt".format(n),"a") as output:
        output.write("\n\n平均実行時間{}s\n".format(sum/num_of_circuit))
        
    os.chdir("/Users/DELL/ソースコード")




print("入力ビットの数を入力してください:",end="")
n = int(input())    
#初期状態を設定
init_state = init_config(n)


#要求出力集合
desired_output_set = [init_state]
os.chdir('/Users/DELL/ソースコード')

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
    os.chdir('/Users/DELL/ソースコード/input/{}'.format(dir_name))
    
    #ファイルから回路を読み込む
    source_circuit = read_file.read_file(file_name)
    circuit = copy.copy(source_circuit)
    print(circuit)
    #回路から要求出力集合を得る
    desired_output_set = desired_output.desired_output(init_state,circuit)
    #回路の最終的な論理状態を取得
    x = logic.logical_state(init_state,circuit)
    #分解前の回路を出力
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
        
        #要求出力が生成されているビットにelementary量子ゲートをつなげる
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
    #display.display_circuit(decomposed_circuit,x)
    print(decomposed_circuit)
    #実行時間を計測
    process_time = time.time() - start
    num_of_circuit += 1
    aggregate.aggregate_result(file_name,source_circuit,decomposed_circuit,n)
    sum += process_time




    print("所要時間:%ds"%process_time)
    
    
end_config(num_of_circuit,sum,n)



