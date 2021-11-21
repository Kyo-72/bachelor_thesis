import random
import display
import desired_output
import os
import shutil

T_GATE_PROB = 5 #Tゲートが挿入されるまでのCNOTの数の期待値
T_GATE_NUM = 3  #Tゲートの数


def generate_gate(n,j,d):
    gate = []
    gate_type = random.randrange(T_GATE_PROB)
    #gate_typeが0ならTゲート
    if(not gate_type or j == d - 1):
        gate = generate_T_gate(n)
        
    #それ以外ならcnotゲート
    else:
        gate = generate_cnot(n)

    return gate



def generate_T_gate(n):
    gate = []
    for i in range(n):
        if(custom_rand(T_GATE_NUM)):
            gate.append( i )

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
    gate.append(c_bit)
    #ターゲットビットを決定（コントロールビットと被らないように）
    while True:
        t_bit = random.randrange(n)
        if(t_bit != c_bit):
            gate.append(t_bit)
            break

    return gate
        
    

# (1/prob) で1を返す
def custom_rand(prob):
    var = random.randrange(prob)
    return (var == 0)

#重複してるゲートを削除
def delete_redundant_gate(str,n):
    #指定したディレクトリのファイル名をリストで取得
    i = 0
    for name in os.listdir(path=str):
        i += 1
        
        
        #ファイル一つずつ調査
        os.chdir('/Users/DELL/ソースコード/input/{}'.format(str))
        with open(name) as f:
            pre_gate = [" "]*n
            with open("circuit{}.txt".format(i),"w") as new_file:
                #ヘッダ書き込み
                new_file.write("#my_test_circuit{}\n".format(i))
                new_file.write(".numvars " + "{}\n".format(n))
                new_file.write(".begin\n")
                
                
                #ゲートをひとつづつ読み込む
                for line in f:
                    gate = line.split(" ")
                    
                   
                    gate_type = gate[0][0]
                    num_of_io = int( gate[0][1] )
                    
       

                    #Tゲートの時

                    if(gate_type == "T"):
                        
                        #直前のゲートと重複していないかチェック
                        
                        delete = 0
                        for bit in gate[1:num_of_io + 1]:
                            
                            t_bit = int(bit)
                            if(pre_gate[t_bit] == 'T'):
                                gate.pop(gate.index(bit))
                                delete += 1
                            else:
                                pre_gate[t_bit] = 'T'
                                

                        if(num_of_io == delete):continue        
                        gate[0] = "T{}".format(num_of_io - delete)

                        
                        new_file.write(gate[0] + " ")
                        for bit in gate[1:-1]:
                            new_file.write( chr( int(bit) + ord("a")) + " ")
                        
                        new_file.write(gate[-1])    
                        

                    #CNOTゲートの時
                    elif(gate_type == "t"):
                        t_bit = int(gate[len(gate)-2])
                        if(pre_gate[t_bit] == line):
                            continue
                        pre_gate[t_bit] = line
                        
                        new_file.write(gate[0] + " ")
                        
                        for bit in gate[1:-1]:
                            new_file.write( chr( int(bit) + ord("a") ) + " " )
                        new_file.write("\n")

                #フッター書き込み
                new_file.write(".end")
                

        #読み込んだ元ファイルを削除
        os.remove(name)
        
            
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
if(exist):
    shutil.rmtree('/Users/DELL/ソースコード/input/{}bit_circuit'.format(n))
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
        gate = generate_gate(n,j,d)
        if(gate != None):
            for g in gate:
                file.write(str(g))
                file.write(" ")

            file.write("\n")
            
    #file.write(".end\n",p)   
    file.close()
    
os.chdir('/Users/DELL/ソースコード/input')
        
#冗長な回路を削除する
delete_redundant_gate("{}bit_circuit".format(n),n)
