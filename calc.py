from pickletools import optimize
from re import A
from z3 import *
import const
from desired_output import desired_output
import display
MAX_NUM_GATE = 20

Q20_graph = [ [1,5],[0,2,6,7],[1,3,6,7],[2,4,8,9],[3,8,9],\
             [0,6,10,11],[1,2,5,7,10,11],[1,2,6,8,12,13],[3,4,7,9,12,13],\
             [3,4,8,14],[5,6,11,15],[5,6,10,12],\
             [7,8,11,13,16,17],[7,8,12,14,18,19],[9,13,18,19],[10,16],\
             [11,12,15,17],[11,12,16,18],[13,14,17,19],[13,14,18] ]

Optimized_nodes = []


# def extract_gate_type(output_set):

#     gate_type = []

#     for output in output_set:
#         gate_type += output[1]


#     return gate_type

# def extract_desired_set(output_set):

#     desired_output= []

#     for output in output_set:
#         desired_output += output[0]

#     desired_output


def nearest_neighbor(c_vec,t_vec,n,s,node):
    
    #使わないノードの情報を無くす(indexエラーを避ける)
    
    for list in node:
        if(type(list) is int):
            break
        delete = []
        tmp = []
        for i in list:
            if(i < n):
                tmp.append(i)
        
        Optimized_nodes.append(tmp)


    
    #コントロールビットがnodeの時の条件を生成
    # for node in range(n):
    #     num_of_near = len(Optimized_nodes[node])
    #     P = Bool("P")
    #     P = t_vec[ Optimized_nodes[node][0] ]
    #     #P = t_vec[ Optimized_nodes[node][0] ]
    #     #print(P)

    #     #ノードiがターゲットビットである条件を生成
    #     for i in Optimized_nodes[node]:
    #         P = Or(P,t_vec[i]) 

    #     print(P)    

    #     s.add(Implies(c_vec[node],P))  
        

def one_bit_per_gate(vec,n,s):
    
    P_vec = [Bool("P_vec%d" % i) for i in range(n)]
    

    for i in range(n):
        P_vec[i] = vec[i]
        for j in range(n):
            if(i != j):
                P_vec[i] = And(P_vec[i],Not(vec[j]))
            
    #全ての制約をorで追加したい
    P = P_vec[0]
    for i in range(1,n):
       P = Or(P,P_vec[i])

    s.add(P)
    
            

def generate_output(f_vec,c_vec,t_vec,d,n):
    
    for d in range(d):
        for i in range(n):
            f_vec[d + 1][i] = f_vec[d][i]
            for j in range(n):
                #iがターゲットビット、jがコントロールビット
                #コントロールビットとターゲットビットが隣接していれば制約を追加
                if(i != j and i in Optimized_nodes[j]):
                    f_vec[d + 1][i] = If(And(t_vec[d][i],c_vec[d][j]),f_vec[d + 1][i]^f_vec[d][j],f_vec[d + 1][i])



def equal_desired_output(f_vec,desired_output,n,d,s,H_gate_vec,T_gate_vec,T_dagger_gate_vec):
    
    i = 0
    for output in desired_output:
        
        P = False
        output_function = abs(output[0])
        gate_tyep = output[1]
        
        #Hゲートなら部分回路の終端の論理関数だけに着目
        if(gate_tyep == const.HADAMARD_GATE):
            for i in range(n):
                P = Or(P, f_vec[d][i] == output_function)
                H_gate_vec[d][i] = (f_vec[d][i] == output_function);

        #Tゲート以外なら部分回路の任意の場所に配置可能
        else: 

            for i in range(d + 1):
                for j in range(n):
                    #括弧ないがそのままゲート変数になる
                    P = Or(P,(f_vec[i][j] == output_function) )
                    if(gate_tyep == const.T_GATE):
                        T_gate_vec[i][j] = (f_vec[i][j] == output_function)
                    elif(gate_tyep == const.T_DAGGER_GATE):
                        T_dagger_gate_vec[i][j] = (f_vec[i][j] == output_function)
            
        s.add(P)

def ex_equal_desired_output(f_vec,output_list,n,d,s):
    #負の数の処理
    for i in range(len(output_list)):
        output_list[i] = abs(output_list[i])
        
    for output in output_list:
        
        #要求出力と出力が正しいかを判定
        s.add(f_vec[d][output_list.index(output)] == output)


def display_bool(c_vec,t_vec,m,d,n):

    for i in range(d):
        for j in range(n):
                    
            print("%d個目、%dライン"%(i+1,j))
            print("%s"%is_true( m[ c_vec[i][j] ] ))
            print("%s"%is_true( m[ t_vec[i][j] ] ))
        print()

def convert_output(m,d,n,c_vec,t_vec):
    output = [[" " for j in range(n)] for i in range(d)]
    
    for i in range(d):
        output
        for j in range(n):
            if(m[c_vec[i][j]] == True):
                output[i][j] = "c"

            if(m[t_vec[i][j]] == True):
                output[i][j] = "t"
                
    return output
    
    # output_circuit = []

    # for i in range(d):

    #     #CNOTゲートを配置
    #     cnot_gate = []
    #     for j in range(n):
    #         if(m[c_vec[i][j]] == True):
    #             cnot_gate.append(const.CONTROLL_BIT)
    #         elif(m[t_vec[i][j]] == True):
    #             cnot_gate.append(const.TARGET_BIT)
    #         else:
    #             cnot_gate.append(" ")

    #     unitary_gate = []
    #     #単位ゲートを配置

    #     for j in range(n):
    #         if( m[ T_gate_vec[i][j] ] ) == True):
    #             unitary_gate.append(const.T_GATE)
    #         elif(m[ T_dagger_gate_vec[i][j] ] == True):
    #             unitary_gate.append(const.T_DAGGER_GATE)
    #         else:
    #             unitary_gate.append(" ")

    #     output_circuit.append(cnot_gate)
    #     output_circuit.append(unitary_gate)

    # H_gate = []
    # #Hゲートを配置
    # for j in range(n):
    #     if(H_gate_vec == True):
    #         H_gate.append(const.HADAMARD_GATE)
    #     else:
    #         H_gate.append(" ")

    # output_circuit.append(H_gate)
                
    # return output_circuit

#i ~ d + 1 j ~ nまでの not T_gate_vec[i][j]をAndでつなげた論理式を生成
def generate_restriction_of_other_gate_position(T_gate_vec,d,n,i,j):

    P = True

    for x in range(i,d + 1):
        for y in range(j,n):
            P = And( P, Not( T_gate_vec[x][y]) )
            
    return P
    


#Tゲートの後にHゲートが来るように調整
def restrict_gate_order(H_gate_vec,T_gate_vec,d,n,s):

    for i in range(d + 1):
        for j in range(n):
            #￢oterh_gate_vec[i][j]をすべてAndでつないだ論理式　i,j以降のT_gate_vecがFalseであるという論理式
            P = generate_restriction_of_other_gate_position(T_gate_vec,d,n,i,j)
            s.add(If(H_gate_vec[i][j],P,True))                                        
                        
            

def calc(input_list,output_set,n,num_of_var,node):

    #TODO　outputからgatetypeと要求出力を取り出すor管理する
    # desired_output = extract_desired_set(output_set)
    # gate_type = extract_gate_type(output_set)
    

    
    d = 0;
    #ゲート数200まで探索
    #論理状態を表現する変数    
    while(d < MAX_NUM_GATE):
        gate = {}

        #d*n CNOTゲート群を表す変数
        c_vec = [[Bool("c_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d)]
        t_vec = [[Bool("t_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d)]
        #ゲートの配置を表す変数
        H_gate_vec = [[Bool("H_gate_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d + 1)]
        T_gate_vec = [[Bool("T_gate_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d + 1)]
        T_dagger_gate_vec = [[Bool("T_dagger_gate_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d + 1)]
        #論理状態を表す変数
        f_vec = [[BitVec("f_vec[%d,%d]" % (i,j),num_of_var) for j in range(n)] for i in range(d + 1)]
        for i in range(n):
        
            f_vec[0][i] =  BitVecVal(input_list[i],num_of_var)
        #z3-solver インスタンスの作成
        s = Solver()

        #このループ　関数内でええやん
        #ゲートごとに制約を追加
        for i in range(d):

            
            #NNA制約式の追加(使わなくていいかも)
            nearest_neighbor(c_vec[i],t_vec[i],n,s,node)
            #同一ゲートはコントロールビットが一つしかない制約
            one_bit_per_gate(c_vec[i],n,s)
            one_bit_per_gate(t_vec[i],n,s)

        
        #出力を生成
        generate_output(f_vec,c_vec,t_vec,d,n)
        #出力と要求出力の一致

        equal_desired_output(f_vec,output_set,n,d,s,H_gate_vec,T_gate_vec,T_dagger_gate_vec)

        #TODO　ここら辺は抜本的に書き換える必要がある
        # restrict_gate_order(H_gate_vec,T_gate_vec,d,n,s)
        
        # if(gate_type == const.HADAMARD_GATE):
        #     ex_equal_desired_output(f_vec,output_list,n,d,s)
        # else:
        #     equal_desired_output(f_vec,output_list,n,d,s)
        #for i in range(n):
            #print("%dline f_vec P :%s"%(i + 1,f_vec[d][i]) )
            
        print("d=%d"%d)
        if(s.check() == sat):
            m = s.model()
            #display_gates(c_vec,t_vec,m,d,n)
            

            return convert_output(m,d,n,c_vec,t_vec)

        d += 1

    
# input = [1,2,4,8]
# output = [(9,"T"),(10,"T"),(6,"T"),(-8,"H"),(10,"H"),(-6,"H"),(-5,"H")]
# n = len(input) 
# display.display_circuit( calc(input,output,n,n) )
