from z3 import *
MAX_NUM_GATE = 10

def nearest_neighbor(c_vec,t_vec,n,s):
    
    for i in range(1,n + 1):
        P = Xor(t_vec[i - 1],t_vec[i + 1])
        s.add(Implies(c_vec[i],P))
        

def one_bit_per_gate(vec,n,s):

    P_vec = [Bool("P_vec%d" % i) for i in range(n + 1)]
    

    for i in range(1,n + 1):
        P_vec[i] = vec[i]
        for j in range(1,n + 1):
            if(i != j):
                P_vec[i] = And(P_vec[i],Not(vec[j]))
            
    #全ての制約をorで追加したい
    P = P_vec[1]
    for i in range(2,n + 1):
       P = Or(P,P_vec[i])

    s.add(P)
    #print(P)
            

def generate_output(f_vec,c_vec,t_vec,d,n):
    
    for d in range(d):
        c_bit = BitVec("c_bit",n + 1)
    
        #dコメのゲート コントロールビットがあればc_bit
        for i in range(1,n + 1):
            c_bit = If(c_vec[d][i],f_vec[i]^c_bit,c_bit)
        for i in range(1,n + 1):
            f_vec[i] = If(t_vec[d][i],c_bit^f_vec[i],f_vec[i])

def equal_desired_output(f_vec,output_list,n,s):
    
    i = 1
    for output in output_list:
        
        P = False
        
        #for j in range(1,n + 1):
        
        P = f_vec[i] == output
        i += 1
        s.add(P)
        #print(P)
        #print("###############################################################")

def display_gates(c_vec,t_vec,m,d,n):

    for j in range(1,n + 1):
    
        for i in range(d):
        
            print("―",end="")
            
        
            C = m[ c_vec[i][j] ]
            T = m[ t_vec[i][j] ]
            if(C == True):
                print("ｃ",end="")
            elif(T == True):
                print("ｔ",end="")
            else:
                print("―",end="")
        print("")

def display_bool(c_vec,t_vec,m,d,n):

    for i in range(d):
        for j in range(1,n + 1):
                    
            print("%d個目、%dライン"%(i+1,j))
            print("%s"%is_true( m[ c_vec[i][j] ] ))
            print("%s"%is_true( m[ t_vec[i][j] ] ))
        print()
                                             
                        
            

def calc(input_list,output_list,n):

    d = 0;
    #ゲート数200まで探索

    #論理状態を表現する変数
    
    f_vec = [BitVec("f_vec%d" % i, n) for i in range(n + 1)]
    for i in range(1,n + 1):
        
        f_vec[i] =  input_list[i]
        
        
    
    while(d < MAX_NUM_GATE):
        gate = {}

        #d*n CNOTゲート群を表す変数
        c_vec = [[Bool("c_vec[%d,%d]" % (i,j)) for j in range(n + 2)] for i in range(d)]
        t_vec = [[Bool("t_vec[%d,%d]" % (i,j)) for j in range(n + 2)] for i in range(d)]
        for i in range(d):
            c_vec[i][0] = False
            t_vec[i][0] = False
            c_vec[i][n + 1] = False
            t_vec[i][n + 1] = False
            
        #z3-solver インスタンスの作成
        s = Solver()

        
        #ゲートごとに制約を追加
        for i in range(d):

            
            #NNA制約式の追加
            nearest_neighbor(c_vec[i],t_vec[i],n,s)
            #同一ゲートはコントロールビットが一つしかない制約
            one_bit_per_gate(c_vec[i],n,s)
            one_bit_per_gate(t_vec[i],n,s)

        
        #出力を生成
        generate_output(f_vec,c_vec,t_vec,d,n)
        #出力と要求出力の一致
        equal_desired_output(f_vec,output_list,n,s)
            
        print("d=%d"%d)
        if(s.check() == sat):
            m = s.model()
            display_gates(c_vec,t_vec,m,d,n)
            
            print("found!")
            return 0
        d += 1

    

input = [0,1,2,4,8,16]
output = [1,2,4,24,16]
n = len(input) - 1


calc(input,output,n)
