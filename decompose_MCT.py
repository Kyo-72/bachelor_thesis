import display
import const
#ancillaにできるbitを探し,その中でターゲットビットとの距離が一番近い,ビットのindexを返す
def search_for_ancilla(line,num_of_io,n,input):
    gate = line.split(" ")[1:num_of_io + 1]
    #コントロールビットを数字で取り出す
    controll_bit = []
    for bit in gate[0:num_of_io - 1]:
        controll_bit.append(input.index(bit))
    
    target_bit = ( input.index(gate[num_of_io - 1].split("\n")[0])) 
    #ancillaにできるビットを探し,target_bitとの距離を入れる
    ancilla = {}

    for i in range(n):
        if( (i not in controll_bit) and i != target_bit):
            #target_bitとancillaの距離
            distance = abs(i - target_bit)
            ancilla[i] = distance
    #distanceが小さい順にソート
    print(ancilla)
    ancilla = sorted(ancilla.items(), key=lambda x:x[1]) 
    res = list(ancilla[0])
    print(type(res[0]))
    #昇順で初めのkeyを返す
    print(res)
    return res[0]  

def convert_mct_into_toffoli(line,num_of_io,n,input):
    gates = ""
    ancilla = search_for_ancilla(line,num_of_io,n,input)
    print("ancilla:{}".format(ancilla))

    bit = line.split(" ")
    #controll_bit一つ目
    a = bit[1]
    #controll_bit二つ目
    b = bit[2]
    #controll_bit三つ目
    c = bit[3]
    #ターゲットビット
    t = bit[4].split("\n")[0]

    gates += "t3 {} {} {}\n".format(a,b,ancilla)
    gates += "t3 {} {} {}\n".format(c,ancilla,t)
    gates += "t3 {} {} {}\n".format(a,b,ancilla)
    gates += "t3 {} {} {}\n".format(c,ancilla,t)
    

    return gates


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
    target_bit = bit[3].split("\n")[0]

    #Clifford+Tゲート群に分解
    gates += "{}1 {}\n".format(const.HADAMARD_GATE,target_bit)
    gates += "{}3 {} {} {}\n".format(const.T_GATE,controll_bit[0],controll_bit[1],target_bit)
    gates += "{}2 {} {}\n".format(const.TARGET_BIT,controll_bit[1],controll_bit[0])
    gates += "{}2 {} {}\n".format(const.TARGET_BIT,target_bit,controll_bit[1])
    gates += "{}2 {} {}\n".format(const.TARGET_BIT,controll_bit[0],target_bit)
    gates += "{}1 {}\n".format(const.T_DAGGER_GATE,controll_bit[1])
    gates += "{}2 {} {}\n".format(const.TARGET_BIT,controll_bit[0],controll_bit[1])
    gates += "{}2 {} {}\n".format(const.T_DAGGER_GATE,controll_bit[0],controll_bit[1])
    gates += "{}1 {}\n".format(const.T_GATE,target_bit)
    gates += "{}2 {} {}\n".format(const.TARGET_BIT,target_bit,controll_bit[1])
    gates += "{}2 {} {}\n".format(const.TARGET_BIT,controll_bit[0],target_bit)
    gates += "{}2 {} {}\n".format(const.TARGET_BIT,controll_bit[1],controll_bit[0])
    gates += "{}1 {}\n".format(const.HADAMARD_GATE,target_bit)

    return gates



def decompose(file_name):
    #分解後回路.最後にファイルに書き込む
    input=[]
    new_circuit = ""
    flag = 0

    with open(file_name) as f:
        
        
        for line in f:
 
            if(".numvars" in line):
               n = int( line.split(" ")[1] )

            if(".variables" in line):
                #量子ビットの上位からinputに入れる
                input = line.split(" ")[1:n + 1]
                #改行文字処理
                input[n - 1] = input[n - 1].split("\n")[0]
        
            #beginからゲートを読み始める(flag = 1)
            if(".begin" in line):
                flag = 1
            #endが来たら読み込み終了
            elif(".end" in line):
                new_circuit += line 
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
                if(type_of_gate == const.TARGET_BIT):
                    
                    #Toffoliゲート分解.
                    if(num_of_io == 3):
                        line = convert_toffoli_into_cnot(line)
                    #MTCゲートをtoffoliに分解後,clifford+tゲート群に分解
                    elif(num_of_io > 3):
                        gate = convert_mct_into_toffoli(line,num_of_io,n,input)
                        gate = gate.split("\n")
                        line = ""
                        for g in gate[:-1]:
                            g += "\n"
                            print(g)
                            line += convert_toffoli_into_cnot(g)
                            

                

            #ゲートを追加
            new_circuit += line 
                    


            

    with open(file_name,mode="w") as f:
        f.write(new_circuit)

    return 0

print("ディレクトリ名を入力してください")
dir = input()

decompose("input/{}/{}.txt".format(dir,dir))
