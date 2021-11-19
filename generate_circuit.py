import random
import display
import desired_output
import os

T_GATE_PROB = 6 #Tゲートが挿入されるまでのCNOTの数の期待値
T_GATE_NUM = 3  #Tゲートの数


def generate_gate(n):
    gate = []
    gate_type = random.randrange(T_GATE_PROB)
    #gate_typeが0ならTゲート
    if(not gate_type):
        gate = generate_T_gate(n)
        
    #それ以外ならcnotゲート
    else:
        gate = generate_cnot(n)

    return gate



def generate_T_gate(n):
    gate = []
    for i in range(n):
        if(custom_rand(T_GATE_NUM)):
            gate.append( chr(ord('a') + i) )

    num = len(gate)
    
    if(not num):
        return None
    
    gate.insert(0,"T{}".format(num))
            
    return gate

def generate_cnot(n):
    gate = []
    gate.append("t2")
    #コントロールビットを決定
    c_bit = random.randrange(n)
    gate.append(chr(c_bit + ord("a")))
    #ターゲットビットを決定（コントロールビットと被らないように）
    while True:
        t_bit = random.randrange(n)
        if(t_bit != c_bit):
            gate.append(chr(t_bit + ord("a")))
            break

    return gate
        
    

# (1/prob) で1を返す
def custom_rand(prob):
    var = random.randrange(prob)
    return (var == 0)

#重複してるゲートを削除
def delete_redundant_gate(str,p):
    #指定したディレクトリのファイル名をリストで取得
    for name in os.listdir(path=str):
        i = 1
        
        #ファイル一つずつ調査
        with open(name) as f:
            pre_gate = [(" "*p)]
            for open("circuit{}".format(i),"w") as new_file
                #ヘッダ書き込み
                new_file.write("#my_test_circuit{}\n".format(i))
                new_file.write(".begin\n")
                i += 1
                #ゲートをひとつづつ読み込む
                for line in f:
                    

    #読み込んだ元ファイルを削除
        
    return 0



#カレントディレクトリを移動
os.chdir('/Users/DELL/ソースコード/input')

print("いくつの回路を生成しますか？: p = ",end="")
p = int( input() )
print("何ビットの回路を生成しますか?: n = ",end="")
n = int( input() )
print("ゲートをいくつ生成しますか?",end="")
d = int ( input() )

exist = os.path.isdir('/Users/DELL/ソースコード/input/{}bit_circuit'.format(n))
if(not exist):
    #bitの数によってディレクトリを分ける
    os.makedirs("{}bit_circuit".format(n))
    


#作成したディレクトリに移動
os.chdir('/Users/DELL/ソースコード/input/{}bit_circuit'.format(n))
for i in range(p):

    #ファイルを書き込み専用で開く
    file = open("test_circuit{}.txt".format(i + 1),'w')
    #ファイルのヘッダに書き込み
    #file.write("#my_test_circuit{}\n".format(i + 1))
    #file.write(".begin\n")
    #回路をd個生成する
    for j in range(d):
        gate = generate_gate(n)
        if(gate != None):
            for g in gate:
                file.write(g + " ")

            file.write("\n")
            
    #file.write(".end\n",p)   
    file.close()
        
    #冗長な回路を削除する
    delete_redundant_gate("{}bit_circuit".format(n))


        

